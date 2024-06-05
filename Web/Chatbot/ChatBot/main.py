from flask import Flask, jsonify, render_template, request, send_file
import subprocess
import os
from flask import *
import requests
import json
import base64
import re

app = Flask(__name__)

upload = r'D:/Web/Chatbot/ChatBot/static/upload'
detect = r'D:/Web/Chatbot/ChatBot/static/detect'


def run_yolo_command(file_name):
    conda_env_path = r'D:\Miniconda\envs\ai_env\python.exe'
    script_path = r'D:\Yolo-v9\yolov9\detect.py'  # Ensure this is the correct path
    weights = r'D:\Yolo-v9\yolov9\yolov9-e.pt'
    source = f"{upload}/{file_name}"
    try:
        result = subprocess.run(
            [conda_env_path, script_path, '--source', source, '--weights', weights, "--project", detect, "--name",
             "result"],
            capture_output=True, text=True)
        output = result.stdout if result.stdout else "No output from script."
        error = result.stderr if result.stderr else "No error from script."
        # Split the response string by the phrase "Results saved to "
        split_parts = error.split("\\")
        desired_path = split_parts[-1]

        # Find the start and end indices of the relevant substring
        start_index = error.find(f"{file_name}:")
        end_index = error.find("Speed:")
        detected_object_string=error[start_index + 19:end_index].strip()
        data = [x.strip() for x in detected_object_string.split(',')]
        data.pop()
        if desired_path[7].isdigit():
            return desired_path[0:8], data
        else:
            return desired_path[0:7], data

    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 400


def chat_with_llava(image_filename, detected_image_path, detected_data):
    original_image_path = f"{upload}/{image_filename}"
    detected_image_path = f"{detect}/{detected_image_path}/{image_filename}"

    with open(original_image_path, "rb") as image_file:
        original_image = base64.b64encode(image_file.read()).decode('utf-8')
    with open(detected_image_path, "rb") as image_file:
        detected_image = base64.b64encode(image_file.read()).decode('utf-8')



    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llava",
        "prompt": f"What is in this first picture?, second picture is first picture's detected object, objects is detected in this first picture is {' '.join(detected_data)}",
        "stream": False,
        "images": [original_image, detected_image]
    }
    response = requests.post(url, data=json.dumps(payload))
    return response.text


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        run_yolo = run_yolo_command(f.filename)
        original_image_path = f"upload/{f.filename}"
        detected_image_path = f"detect/{run_yolo[0]}/{f.filename}"
        response = chat_with_llava(f.filename, run_yolo[0], run_yolo[1])
        response_text = json.loads(response)["response"]
        #return render_template("Acknowledgement.html", original_image=f.filename, data=response_text)
        #print(run_yolo)
        return render_template("Acknowledgement.html", original_image=original_image_path,
                               detected_image=detected_image_path, data=response_text, detected_image_data=run_yolo[1])


@app.route('/')
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
