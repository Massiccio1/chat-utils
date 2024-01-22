from flask import Flask, redirect, request, jsonify, render_template, send_from_directory, url_for
from flask_cors import CORS, cross_origin
import my_utils
import numpy as np
import os
import json
import os

app = Flask(__name__,
            static_folder='img',
            template_folder='views')
cors = CORS(app)

def get_filenames(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def create_folder(folder_name):
    # Check if the folder already exists
    if not os.path.exists(folder_name):
        # If not, create the folder
        os.makedirs(folder_name)
        # print(f"Folder '{folder_name}' created successfully.")
    else:
        # print(f"Folder '{folder_name}' already exists.")
        pass
    

@app.route("/")
@app.route('/index', methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')



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



# @app.route('/', methods=['GET'])
# @cross_origin()
# def home():
#     return redirect("/index")


@app.route('/chat', methods=['GET', 'POST'])
@cross_origin()
def chat():
    # print("in chat")
    folder_path = 'chat'  # Change this to the path of the folder you want to read

    if request.method == 'POST':
        selected_filename = request.form['filename']
        search = request.form['search']
        
        file_content="placeholder"
        
        if search!="":  
            id = selected_filename[:-5]     #remove .html
            file_content = my_utils.build_html(id, selected_filename, search, False)
            return render_template('file.html', filenames=get_filenames(folder_path), selected_filename=selected_filename, file_content=file_content)

        else:
            # print("search for: ",search)
            file_path = os.path.join(folder_path, selected_filename)

            # Read the content of the selected file
            with open(file_path, 'r') as file:
                file_content = file.read()

            return render_template('file.html', filenames=get_filenames(folder_path), selected_filename=selected_filename, file_content=file_content)

    return render_template('file.html', filenames=get_filenames(folder_path))

@app.route('/info', methods=['GET', 'POST'])
@cross_origin()
def info():
    # print("in chat")
    folder_path = 'info'  # Change this to the path of the folder you want to read
    files = get_filenames(folder_path)
    # return {"data":files}
    html=""
    for f in files:
        with open(f'{folder_path}/{f}') as json_file:
            data = json.load(json_file)
        
            # Print the type of data variable
            html = html + f'<br>id: {data["id"]}<br>url: {data["url"]}<br>title: {data["title"]}<br><img src="{data["thumbnail"]}"><br>timestamp: {data["timestamp"]}<br>date: {data["datetime"]}<br>duration: {data["duration"]}<br>-----------------------------------------------<br>'
        
            # Print the data of dictionary
        
            
    return html

if __name__ == '__main__':
    create_folder("chat")
    create_folder("raw_csv")
    create_folder("csv")
    create_folder("img")
    create_folder("data")
    create_folder("info")
    app.run(host='0.0.0.0',port=8060)