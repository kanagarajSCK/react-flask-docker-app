from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import os
from face_detector import detect_age_gender

app = Flask(__name__, static_folder='build', static_url_path='/')
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result_img_base64, detections = detect_age_gender(img)
    return jsonify({'image': result_img_base64, 'detections': detections})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

























# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import numpy as np
# import cv2
# from face_detector import detect_age_gender

# app = Flask(__name__)
# CORS(app)

# @app.route('/detect', methods=['POST'])
# def detect():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
#     file = request.files['image']
#     npimg = np.frombuffer(file.read(), np.uint8)
#     img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     result_img_base64, detections = detect_age_gender(img)

#     return jsonify({'image': result_img_base64, 'detections': detections})

# if __name__ == '__main__':
#     app.run(debug=True)
    
    