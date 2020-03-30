import pickle
import hashlib
import numpy as np
from skimage import io
import face_recognition
from flask import Flask, request, jsonify

app = Flask(__name__)

def hash_encoding(encoding):
    # Generate md5 hash from string encoded array
    en_hash = hashlib.md5(str(encoding).encode())
    # Return readable hexdigest of hash
    return en_hash.hexdigest()

def sapien_identifier(url):
    # Load unknown image from given URL
    unknown_image = io.imread(url)
    # Generate face encoding for unknown image
    if len(face_recognition.face_encodings(unknown_image)):
        # Check if a face exists in the image
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    else:
        # If no face is detected return None
        return None
    try:
        # Try to load pickle file, if it exists
        sapien_encodings = pickle.load(open("sap.pkl", "rb"))
        for i in range(0, len(sapien_encodings)):
            # Compare encoding with all known encodings in the database
            results = face_recognition.compare_faces([sapien_encodings[i]], unknown_encoding)
            if results[0]:
                # Hash original face encoding from pickle file and search for hex id
                return hash_encoding(sapien_encodings[i])
                # Break out of loop
                break
            else:
                try:
                    # Check if next element is available
                    next_element = sapien_encodings[i+1]
                    # If next element is available continue with loop
                    pass
                except IndexError:
                    # Since next element is not available, add face to DB
                    pickle.dump(np.vstack((sapien_encodings, unknown_encoding)), open("sap.pkl", "wb"))
                    # Return hash of unknown face encoding
                    return hash_encoding(unknown_encoding) 
    except (OSError, IOError) as e:
        # If the pickle file doesn't exist, create and dump encoding
        pickle.dump(np.array([unknown_encoding]), open("sap.pkl", "wb"))
    # Return hash of unknown face encoding
    return hash_encoding(unknown_encoding)
    

@app.route('/', methods=['GET', 'POST'])
def recognition_manager():
    if request.method == 'GET':
        # Handle GET request
        return 'Received GET request, endpoint is POST only.'
    elif request.method == 'POST':
        # Get the JSON request
        personal_data = request.get_json()
        # Get the identifier
        personal_id = personal_data['id']
        # Get the image URL
        personal_image = personal_data['image']
        # Retrieve facehash
        face_hash = sapien_identifier(personal_image)
        # Brew response
        response = {'facehash': face_hash, 'id': personal_data['id']}
        return jsonify(response)
    else:
        # Handle non-GET and POST requests
        return 'BAD REQUEST.'


if __name__ == "__main__":
    # Run server
    app.run(host="0.0.0.0", port=80)