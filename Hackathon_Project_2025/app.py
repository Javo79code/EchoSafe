from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

# Flask App
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Folder to save uploaded audio
UPLOAD_FOLDER = os.path.join('static', 'uploads')  # <- Correct way
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Javahir2004$!",
    database="scam_voice_db"
)
cursor = db.cursor()

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Add Scammer Page
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        voice_id = request.form['voice_id']
        audio = request.files['audio']

        if name == '' or voice_id == '' or audio.filename == '':
            flash('All fields are required!', 'danger')
            return redirect(url_for('add'))

        if audio and allowed_file(audio.filename):
            filename = secure_filename(audio.filename)

            # Final fix: Get full path
            save_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            audio_full_path = os.path.join(save_path, filename)
            audio.save(audio_full_path)

            # Save relative path for database
            audio_path = f"static/uploads/{filename}"

            sql = "INSERT INTO scammers (name, voice_id, audio_file_path) VALUES (%s, %s, %s)"
            val = (name, voice_id, audio_path)
            cursor.execute(sql, val)
            db.commit()

            flash('Scammer Added Successfully!', 'success')
            return redirect(url_for('add'))
        else:
            flash('Invalid file format! Please upload .mp3 or .wav only.', 'danger')
            return redirect(url_for('add'))

    return render_template('add.html')

# Search Scammer Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    result = None
    if request.method == 'POST':
        voice_id = request.form['voice_id']
        sql = "SELECT * FROM scammers WHERE voice_id = %s"
        val = (voice_id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
    return render_template('search.html', result=result)

# View All Scammers
@app.route('/view')
def view():
    cursor.execute("SELECT * FROM scammers")
    scammers = cursor.fetchall()
    return render_template('view.html', scammers=scammers)

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
