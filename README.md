# Image-Story

## Overview
This web application allows users to upload an image and receive information about the contents of the image. It utilizes two advanced AI tools, Yolov9 for object detection and Llava (Ollama's model) for image analysis.

## How It Works
1. **Upload Image**: Users can upload an image through the web interface.
2. **Object Detection**: The Yolov9 tool processes the image to detect objects.
3. **Image Analysis**: The original image, along with the detected image and objects, are sent to Llava to interpret what's inside the image.
4. **Results**: The application displays the analysis results, and detected image to the user.

## FlowChart
1. User choose a image from static/upload
2. Program run yolo to get detected image and a list of detected object (object and object's quantity)
3. Progran call API to Ollama with detected image and list of detected objects
4. Render to HTML file with detected image and list of detected objects
5. In HTML, display original image, detected image and list of detected objects in this image. 

## Built With
- **Anaconda(Mini)**: An open-source distribution of Python and R for scientific computing.
- **Llava (Ollama's model)**: AI tool for general-purpose visual and language understanding.
- **Yolo-V9**: Cumputer Vision AI tool for detecting object in image and video.
- **Flask**: A micro web framework written in Python.

## Getting Started
To get a local copy up and running, follow these simple steps.

### Prerequisites
- Anaconda (Optional)
- LLava
- Yolo-V9
- Flask

### Installation
1. Install Ollama 
- On Windown: Download .exe file from https://ollama.com/
- On Anaconda: run commands 
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install ollama
2. Run Llava via Ollama
- Ollama run llava
3. Clone Yolov9 from Github (https://github.com/WongKinYiu/yolov9)
- git clone https://github.com/WongKinYiu/yolov9.git
4. Install Flask
- pip install flask

### Usage
1. Create and Activate the Anaconda environment
2. Run Yolo requirements.txt file
3. Move all images to Image-Story\Web\Chatbot\ChatBot\static\upload
- Because Flask is designed to handle static files, including images, in a specific way. 
- By default, Flask looks for static files in the static directory within your application’s root directory
4. Start Ollama server
5. Run the Flask application

### Acknowledgements
1. Working on Anaconda environment
2. Use Flask to run Yolo-V9
3. Use Ollama by calling API

