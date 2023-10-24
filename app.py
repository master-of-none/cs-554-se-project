from flask import Flask, request, render_template
import os
from typing import Sequence
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google-cloud-vision-credentials.json'

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def analyze_image_from_uri(
        image_uri: str,
        feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    rq = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=rq)

    return response

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
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)
            features = [vision.Feature.Type.TEXT_DETECTION]
            response = analyze_image_from_uri(image_path, features)
            text = detect_text(response)
            return render_template('result.html', image_path=image_path, extracted_text=text)

    return render_template('index.html')

def detect_text(response: vision.AnnotateImageResponse):
    print("=" * 80)
    string = ""
    for annotation in response.text_annotations:
        vertices = [f"({v.x},{v.y})" for v in annotation.bounding_poly.vertices]
        string.join(f"{repr(annotation.description):42} | {', '.join(vertices)}\n")
    return string


if __name__ == '__main__':
    app.run(debug=True)
