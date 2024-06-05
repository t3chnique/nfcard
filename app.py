import os
import uuid
# import requests
import json
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask import (Flask, render_template, request,
                   redirect, url_for, send_from_directory)
from datetime import datetime


# random_filename = str(uuid.uuid4())
current_date = datetime.now().strftime('%d.%m.%y')
file_type = "video"
# file_name = f'{current_date}_{file_type}_{random_filename}'

app = Flask(__name__)
# Setup Flask-Limiter
'''
limiter = Limiter(
    app,
    key_func=get_remote_address,  # Use the user's IP address to track
    default_limits=["2 per 5 minutes"]  # Set the rate limit
)
'''
app.config['UPLOAD_FOLDER'] = 'uploads'

with open("main.json", "r", encoding="utf-8") as file:
    ascii_json = json.load(file)
keyboard = ascii_json["keyboard"]
bj = ascii_json["bj"]
police = ascii_json["police"]
devider = ascii_json["devider"]
kabluki = ascii_json["kabluki"]
kabluki2 = ascii_json["kabluki2"]
legla = ascii_json["legla"]


def allowed_file(filename):
    # Add other popular video formats as needed
    ALLOWED_EXTENSIONS = {'avi', 'flv', 'wmv', 'mov', 'mp4',
                          'm4v', 'mpeg', 'mpg', 'mkv', 'webm'}
    return '.' in filename and filename.rsplit('.',
                                               1)[1].lower(
                                                   ) in ALLOWED_EXTENSIONS


# Define the maximum allowed file size in bytes (e.g., 10 MB)
MAX_FILE_SIZE_BYTES = 1000 * 1024 * 1024  # 1 GB
# Define the maximum allowed total folder size in bytes (e.g., 100 MB)
MAX_FOLDER_SIZE_BYTES = 10000 * 1024 * 1024  # 10 GB


@app.route('/')
def index():
    return render_template('index.html', kabluki=kabluki)


@app.route('/status')
def status():
    message = ""
    message += "Hello!"
    if current_date:
        message += "<br>current_date: works"
    if status:
        message += ("<br>File size limit: "
                    f"{round(MAX_FILE_SIZE_BYTES/1000000/1000)} GB, "
                    "Folder size limit: "
                    f"{round(MAX_FOLDER_SIZE_BYTES/1000000/1000)} GB")
    return message


@app.route('/example', methods=['POST'])
def example():
    # Pass the filename of the example video to the template
    return render_template('example.html')


def get_total_files_size(folder):
    total_size = 0
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size


@app.route('/upload', methods=['POST'])
def upload_file():
    error_message = "<br>try shorter video or text us (https://t.me/levaau)"
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Calculate the total size of files in the uploads folder
        total_folder_size = sum(os.path.getsize
                                (os.path.join(app.config['UPLOAD_FOLDER'], f))
                                for f in os.listdir
                                (app.config['UPLOAD_FOLDER']))
        # Calculate the size of the new file
        new_file_size = len(file.read())
        # Check if adding the new file exceeds the maximum folder size
        if total_folder_size + new_file_size > MAX_FOLDER_SIZE_BYTES:
            return ('The total size of uploaded files exceeds the '
                    'maximum allowed size '
                    f'({round(MAX_FOLDER_SIZE_BYTES/1024/1024)} MB)'
                    f'{error_message}')
        # Check if the file size exceeds the maximum allowed size
        if new_file_size > MAX_FILE_SIZE_BYTES:
            return ('File size exceeds the maximum allowed size '
                    f'({round(MAX_FILE_SIZE_BYTES/1024/1024)} MB)'
                    f'{error_message}')

        filename = current_date + file_type + str(uuid.uuid4()) + '.mp4'
        file.seek(0)  # Reset file pointer to the beginning before saving
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        '''
        try:
            user_ip = request.remote_addr
            response = requests.get(f'http://ip-api.com/json/{user_ip}')
            data = response.json()
            e = " no"
            txt_recorder(filename, user_ip, response, data, e)
        except Exception as e:
            txt_recorder(e)
        information = '------------\nvideo uploaded'
        txt_editor(filename, information)
        '''
        return redirect(url_for('congrats', filename=filename))
        # return redirect(url_for('play_video', filename=filename))
    else:
        return 'Invalid file type'


@app.route('/congrats/<filename>')
def congrats(filename):
    return render_template('congrats.html', legla=legla, filename=filename)


@app.route('/videos/<filename>', methods=['POST'])
def play_video_now(filename):
    return render_template('video.html', filename=filename)


@app.route('/videos/<filename>')
def play_video(filename):
    return render_template('video.html', filename=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


'''
def txt_recorder(filename, user_ip, response, data, e):
    with open(f'{filename}.txt', 'w') as file:
        # Write the text "hello world" to the file
        file.write(f"hello, {user_ip}.\nresponse: {response}"
                   f"\ndata:{data}\ne:{e}")


def txt_editor(filename, information):
    with open(f'{filename}.txt', 'a') as file:
        # Write additional information to the file
        file.write(f"\n{information}")
'''


@app.route('/11fc61524c04d79baf0b9eb9c9dd3d6')
def admin():
    # Get the list of files in the uploads folder
    upload_folder = app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_folder)
    return render_template('admin.html', bj=bj, files=files)


@app.route('/delete', methods=['POST'])
def delete_file():
    # Get the list of files to delete from the form data
    files_to_delete = request.form.getlist('file')
    upload_folder = app.config['UPLOAD_FOLDER']
    for file in files_to_delete:
        file_path = os.path.join(upload_folder, file)
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
