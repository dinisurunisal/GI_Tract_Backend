import flask
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from flask_cors import CORS
from flask import Flask, send_file, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'F:/FYP/gi-tract-backend/assets/uploads/'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

classes = ['esophagitis-a', 'polyps', 'barretts-short-segment',
 'ulcerative-colitis-grade-3', 'ulcerative-colitis-grade-1-2',
 'ulcerative-colitis-grade-2', 'bbps-0-1', 'barretts',
 'ulcerative-colitis-grade-0-1', 'dyed-resection-margins',
 'ulcerative-colitis-grade-2-3', 'retroflex-rectum', 'retroflex-stomach',
 'ulcerative-colitis-grade-1', 'z-line', 'hemorrhoids', 'pylorus',
 'impacted-stool', 'bbps-2-3', 'ileum', 'cecum', 'esophagitis-b-d',
 'dyed-lifted-polyps']

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

@app.route('/send', methods=['POST'])
def send():
    print('send')
    extracted_name = 'test.jpeg'
   
    return send_file(extracted_name, mimetype="image/jpeg")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Validate whether the POST request have a file
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({ 'message': 'Please upload a file!', 'valid': False })
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return jsonify({ 'message': 'Please upload a file!', 'valid': False })

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': 'Uploaded the file successfully: ' + file.filename, 'valid': True})

    return jsonify({ 'message': 'Could not upload the file !', 'valid': False  })

# prediction API
@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            if 'file' not in request.files:
                return "Please try again. The Image doesn't exist"
            
            file = request.files.get('file')

            if not file:
                return

            img_bytes = file.read()
            img = prepare_image(img_bytes)

            class_result , prob_result = predict_result(img)
            predictions = {
                "imageName": secure_filename(file.filename),
                "class1":class_result[0],
                "class2":class_result[1],
                "class3":class_result[2],
                "prob1": prob_result[0],
                "prob2": prob_result[1],
                "prob3": prob_result[2],
            }

            return jsonify(
                {'prediction': predictions}
                )

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((128, 128))
    img = np.array(img)
    img = img.astype('float32')
    img = img/255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_result(img):
    prediction = model.predict(img)
    highest_pred = np.max(prediction)
    pred_idx = np.argmax(prediction).astype(np.uint8)

    dict_result = {}
    for i in range(23):
        dict_result[prediction[0][i]] = classes[i]

    res = prediction[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]

    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])
    return class_result, prob_result

if __name__ == "__main__":
    model_path = "F:\FYP\gi-tract-backend\models\model_final.h5"
    model = tf.keras.models.load_model(model_path)
    print ('Model loaded')
    # model_columns = joblib.load(model_columns_file_name) # Load "model_columns.pkl"
    # print ('Model columns loaded')
    app.run(port=5000, debug=True)
