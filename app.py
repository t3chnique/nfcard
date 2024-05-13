import os
import uuid
from flask import (Flask, render_template, request,
                   redirect, url_for, send_from_directory)
from datetime import datetime

random_filename = str(uuid.uuid4())
current_date = datetime.now().strftime('%d.%m.%y')
file_type = "video"
file_name = f'{current_date}_{file_type}_{random_filename}'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp4'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    message = ""
    message += "Hello!"
    if file_name:
        message += "<br>File_name: works"

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
    # Define the maximum allowed file size in bytes (e.g., 10 MB)
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
    # Define the maximum allowed total folder size in bytes (e.g., 20 MB)
    MAX_FOLDER_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

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
                    '<br>try video that is less 1 min lenghts')
        # Check if the file size exceeds the maximum allowed size
        if new_file_size > MAX_FILE_SIZE_BYTES:
            return ('File size exceeds the maximum allowed size '
                    f'({round(MAX_FILE_SIZE_BYTES/1024/1024)} MB)'
                    '<br>try video that is less 1 min lenghts')

        filename = str(uuid.uuid4()) + '.mp4'
        file.seek(0)  # Reset file pointer to the beginning before saving
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('user_menu', filename=filename))
        # return redirect(url_for('play_video', filename=filename))
    else:
        return 'Invalid file type'


@app.route('/user_menu/<filename>')
def user_menu(filename):
    return render_template('user_menu.html', filename=filename)


@app.route('/videos/<filename>', methods=['POST'])
def play_video(filename):
    return render_template('video.html', filename=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


'''
@app.route('/mutant')
def admin():
    # Get the list of files in the uploads folder
    upload_folder = app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_folder)
    return render_template('admin.html', files=files)


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
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
