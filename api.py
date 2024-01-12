from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import my_utils
import numpy as np

app = Flask(__name__,
            static_folder='img',
            template_folder='views')
cors = CORS(app)

@app.route('/parse_request', methods=['POST'])
@cross_origin()
def parse_request():
    try:
        # Assuming the request contains a JSON body
        print("inizio")
        request_data = request.get_json()
        print("parsed")
        # Accessing values from the JSON body
        value1 = request_data.get('key1')
        value2 = request_data.get('key2')

        # Do something with the values (e.g., print or process)
        print(f"Value 1: {value1}")
        print(f"Value 2: {value2}")

        # You can also return a response
        response = {
            'success': True,
            'message': 'Request successfully processed',
            'data': {
                'value1': value1,
                'value2': value2
            }
        }

        return jsonify(response)

    except Exception as e:
        # Handle exceptions if needed
        response = {
            'success': False,
            'message': f'Error: {str(e)}'
        }

        return jsonify(response)
    
@app.route('/parse', methods=['POST'])
@cross_origin()
def parse():
    try:
        # Assuming the request contains a JSON body
        print("inizio")
        request_data = request.get_json()
        print("parsed: ", request_data)
        # Accessing values from the JSON body
        url = request_data.get('url')
        prominence = request_data.get('prominence')
        range = request_data.get('range')
        # Do something with the values (e.g., print or process)
        print(f"got url: {url}")
        print(f"got prominence: {prominence}")
        print(f"got range: {range}")

        id, peaks, title = my_utils.parse(url, prominence/100, range)
        print("url: ", url, "\npeaks: ", peaks)

        # You can also return a response
        response = {
            'success': True,
            'message': 'Request successfully processed',
            'data': {
                'id': id,
                'peaks': peaks,
                'range': range,
                "title": title
            }
        }

        return jsonify(response)

    except Exception as e:
        # Handle exceptions if needed
        response = {
            'success': False,
            'message': f'Error: {str(e)}'
        }

        return jsonify(response)
    
@app.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({"response":"status ok"})

@app.route('/index', methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8060)