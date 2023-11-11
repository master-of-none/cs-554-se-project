import io
import json

from flask import Flask, jsonify, request, render_template
import os
from google.cloud import vision, vision_v1
from google.cloud import translate
import pycountry

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
            return render_template('result.html', image_path=image_path, extracted_text=text,
                                   detectedLanguage=detect_extracted_language(text))

    return render_template('index.html')


def detect_extracted_language(extracted_text):
    with open(r'google-cloud-vision-credentials.json', 'r') as json_file:
        credentials = json.load(json_file)

    project_id = credentials.get('project_id')
    parent = f"projects/{project_id}"
    client = translate.TranslationServiceClient()
    response = client.detect_language(parent=parent, content=extracted_text)
    language_code = response.languages[0].language_code
    if "-" in language_code:
        # Split the code into 2 parts to find the language name for the primary part
        primary_code = language_code.split('-')[0]
        language = pycountry.languages.get(alpha_2=primary_code)
    else:
        language = pycountry.languages.get(alpha_2=language_code)
    return language.name

@app.route('/translate', methods=['POST'])
def translate_text():
    extracted_text = request.form.get('extracted_text')
    target_language = request.form.get('target_language')

    with open(r'google-cloud-vision-credentials.json', 'r') as json_file:
        credentials = json.load(json_file)

    project_id = credentials.get('project_id')
    parent = f"projects/{project_id}"
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        parent=parent,
        contents=[extracted_text],
        target_language_code=target_language,
    )
    translated_text = response.translations[0].translated_text

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
