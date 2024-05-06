# import random
import uuid
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os


random_filename = str(uuid.uuid4())
current_date = datetime.now().strftime('%d.%m.%y')
file_type = "video"
file_name = f'{current_date}_{file_type}_{random_filename}'


app = Flask(__name__)
app.secret_key = random_filename
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/status')
def status():
    message = ""
    message += "Hello!"
    if file_name:
        message += "<br>File_name: works"

    return message


'''
@app.route('/video', methods=['POST'])
def video():
    return render_template('video.html')
'''


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/step1', methods=['POST'])
def step1():
    return render_template('step1.html')


@app.route('/step2', methods=['POST'])
def step2():
    username = request.form['username']
    session['username'] = username
    message = f"Hello, {username}!"
    return render_template('step2.html', message=message)


@app.route('/step3', methods=['POST'])
def step3():
    filename = request.form['filename']
    session['filename'] = filename
    return render_template('step3.html')


@app.route('/submit', methods=['POST'])
def submit():
    # 1. Get the uploaded file from the request
    file = request.files['file']

    # 2. Check if a file was selected
    if file.filename == '':
        return 'No file selected'

    # 3. Validate file extension (ensure it's .mp4)
    if file and allowed_file(file.filename):
        # 3a. Secure the filename to prevent potential attacks
        filename = secure_filename(file.filename)

        # 3b. Generate UUID for unique directory
        video_uuid = str(uuid.uuid4())
        video_dir = os.path.join(app.config['UPLOAD_FOLDER'], video_uuid)
        os.makedirs(video_dir, exist_ok=True)

        # 3c. Save the file to the generated directory
        file.save(os.path.join(video_dir, filename))

        # 3d. Create the HTML file for the video
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Page</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
    </style>
</head>
<body>
    <video autoplay loop controls>
        <source src="/video/{video_uuid}/{filename}" type="video/mp4">
        <!-- Add additional source tags for different video formats -->
        Your browser does not support the video tag.
    </video>
</body>
</html>
"""
        # 3e. Save the HTML content to the generated directory
        with open(os.path.join(video_dir, "index.html"), "w") as f:
            f.write(html_content)

        # 3f. Return a success message with the video URL
        return f"Video uploaded and page created at: /video/{video_uuid}"

    # 4. If the file type is not allowed, return an error message
    return 'Invalid file type. Please upload a .mp4 file.'


@app.route('/video/<uuid:video_uuid>/<filename>')
def video_file(video_uuid, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(video_uuid)), filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp4'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
