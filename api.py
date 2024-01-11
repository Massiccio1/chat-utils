from flask import Flask, request, jsonify

import my_utils
import numpy as np

app = Flask(__name__)

@app.route('/parse_request', methods=['POST'])
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
def parse():
    try:
        # Assuming the request contains a JSON body
        print("inizio")
        request_data = request.get_json()
        print("parsed")
        # Accessing values from the JSON body
        url = request_data.get('url')
        # Do something with the values (e.g., print or process)
        print(f"got url: {url}")

        id, peaks = my_utils.parse(url)

        # You can also return a response
        response = {
            'success': True,
            'message': 'Request successfully processed',
            'data': {
                'id': id,
                'peaks': np.array2string(peaks)
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
def status():
    return jsonify({"response":"status ok"})

if __name__ == '__main__':
    app.run(host='192.168.1.10',port=8060)