from flask import Flask, render_template, request, make_response
import cv2
import numpy as np
import datetime
from camera import get_frame #Import get_frame from camera.

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

def send_file_data(data, mimetype='image/jpeg', filename='output.jpg'):
    
    response = make_response(data)
    response.headers.set('Content-Type', mimetype)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    
    return response
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        fs = request.files.get('snap')
        if fs:
            img = cv2.imdecode(np.frombuffer(fs.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            img = get_frame(img)
            ret, buf = cv2.imencode('.jpg', img)
            return send_file_data(buf.tobytes())
        else:
            return 'You forgot Snap!'
    
    return 'This page is unavailable to users.'
    
    
 
app.run()