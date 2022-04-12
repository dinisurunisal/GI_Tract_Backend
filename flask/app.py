import flask
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, send_file, jsonify, request 

app = Flask(__name__)

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

@app.route('/predict', methods=['POST']) # Your API endpoint URL would consist /predict
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
            # json_ = request.json
            # query = pd.get_dummies(pd.DataFrame(json_))
            # query = query.reindex(columns=model_columns, fill_value=0)

            # prediction = list(lr.predict(query))

            return jsonify({'prediction': predict_result(img)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((128, 128))
    img = np.array(img)
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
    return class_result[0]

if __name__ == "__main__":
    model_path = "F:\FYP\gi-tract-backend\mode_resenet.h5"
    model = tf.keras.models.load_model(model_path)
    print ('Model loaded')
    # model_columns = joblib.load(model_columns_file_name) # Load "model_columns.pkl"
    # print ('Model columns loaded')
    app.run(port=5000, debug=True)
