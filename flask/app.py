from flask import Flask, send_file

app = Flask(__name__)

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

@app.route('/send', methods=['POST'])
def send():
    print('send')
    extracted_name = 'test.jpeg'
   
    return send_file(extracted_name, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
