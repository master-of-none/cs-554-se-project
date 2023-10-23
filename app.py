from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Creating a folder for storing files to be uploaded
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the allowed extensions are png and jpg
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_types(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file found"
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected"
        
        if allowed_types(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return "File uploaded successfully"
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
