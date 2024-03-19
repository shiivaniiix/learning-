from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Add this line to set the configuration

# Configure SQLite database
DATABASE = 'documents.db'

def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    file_path TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    conn.close()
    return render_template('index.html', documents=documents)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Use app.config to access the configuration
        file.save(file_path)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO documents (name, file_path) VALUES (?, ?)", (filename, file_path))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
