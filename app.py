import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
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
    return render_template('example.html', filename='amisrael.mp4')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.mp4'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('play_video', filename=filename))
    else:
        return 'Invalid file type'


@app.route('/videos/<filename>')
def play_video(filename):
    return render_template('video.html', filename=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
