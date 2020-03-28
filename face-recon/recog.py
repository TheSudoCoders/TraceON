import face_recognition
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def recognition_manager():
    if request.method == 'GET':
        # Handle GET request
        return 'Received GET request, endpoint is POST only.'
    elif request.method == 'POST':
        # Get the JSON request
        personal_data = request.get_json()
        # Get the identifier
        personal_id = personal_data["id"]
        # Get the image URL
        personal_image = personal_data["image"]
        # TODO: Check against known faces
    else:
        # Handle non-GET and POST requests
        return 'BAD REQUEST.'
