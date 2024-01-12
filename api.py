from flask import Flask, redirect, request, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import my_utils
import numpy as np
import os

app = Flask(__name__,
            static_folder='img',
            template_folder='views')
cors = CORS(app)

def get_filenames(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]




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
    

@app.route('/readFile/<filename>')
def read_file(filename):
    file_path = os.path.join('csv', filename)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    else:
        return jsonify(error='File not found'), 404

@app.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({"response":"status ok"})

@app.route('/index', methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/file')
@cross_origin()
def file():
    folder_path = './chat'  # Change this to the path of the folder you want to read

    # Get all filenames in the folder
    filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    return render_template('file.html', filenames=filenames)

# @app.route('/', methods=['GET'])
# @cross_origin()
# def home():
#     return redirect("/index")


@app.route('/chat', methods=['GET', 'POST'])
@cross_origin()
def tmp():
    folder_path = 'chat'  # Change this to the path of the folder you want to read

    if request.method == 'POST':
        selected_filename = request.form['filename']
        file_path = os.path.join(folder_path, selected_filename)

        # Read the content of the selected file
        with open(file_path, 'r') as file:
            file_content = file.read()

        return render_template('file.html', filenames=get_filenames(folder_path), selected_filename=selected_filename, file_content=file_content)

    return render_template('file.html', filenames=get_filenames(folder_path))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8060)