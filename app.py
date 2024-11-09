from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'wmv'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
    return render_template('index.html')

@app.route('/redirect_page', methods=['GET', 'POST'])
def show_redirect_page():
    show_register_fields = False
    if request.method == 'POST':

        # Обработка формы здесь
        print(request.form)
        # Пример: если форма отправлена, показать поля регистрации
        show_register_fields = True

    return render_template('redirect_page.html', show_register_fields=show_register_fields)

if __name__ == '__main__':
    app.run(debug=True)