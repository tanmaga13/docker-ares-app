from flask import Flask, jsonify, request, render_template
import os 
import json
from business import get_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api():
    data = get_data()
    data = {
        'data': data
    }

    return jsonify(data)


if __name__== "__main__ ":
    app.run(port=8000, host = '0.0.0.0', debug=True)