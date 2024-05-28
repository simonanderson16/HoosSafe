from django.apps import AppConfig
from flask import Flask, request, render_template

app = Flask(__name__)


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import create_custom_user_if_not_exists

        from django.contrib.auth import user_logged_in
        user_logged_in.connect(create_custom_user_if_not_exists)


# Route to render the upload form
@app.route('/')
def upload_form():
    return render_template('report_form.html')


# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Save the file to the uploads folder
    file.save('uploads/' + file.filename)

    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
