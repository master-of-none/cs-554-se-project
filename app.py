import io
from flask import Flask, request, render_template
import os
from google.cloud import vision, vision_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google-cloud-vision-credentials.json'

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def detect_text(img):
    client = vision.ImageAnnotatorClient()
    with io.open(img, 'rb') as image_file:
        content = image_file.read()
    image = vision_v1.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    extracted_text = ""
    for text in texts:
        extracted_text = text.description.replace("\n", "<br>")
        break  # Only use the first result
    return extracted_text


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
            image_path = file.filename
            file.save(image_path)
            text = str(detect_text(image_path))
            return render_template('result.html', image_path=image_path, extracted_text=text)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
