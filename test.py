import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import classify
import convert

#HEADPHONE TYPES: Over Ear, On Ear, IEM

#OVER EAR: Portable, or Not (powered by DAC + AMP) => SOUND SIGNATURE => show results

#ON EAR: CLOSED-BACK, OPEN-BACK, GRADOS => SOUND SIG => SHOW RESULTS

#IEM: OVER EAR, STRAIGHT DOWN => SOUND SIGNATURE => SHOW RESULTS


UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)

@app.route('/', methods=['GET'], defaults={'path': 'index.html'})
@app.route('/<path>', methods=['GET'])
def index(path):
    return send_from_directory('static', path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    f = request.files['file']
    mp3name = secure_filename(f.filename)
    f.save(os.path.join(UPLOAD_FOLDER, mp3name))
    wavname = mp3name[:len(mp3name) - 4] + ".wav"
    convert.convert(mp3name, wavname)

    classification = classify.runClassify(wavname)
    os.remove(os.path.join(UPLOAD_FOLDER, wavname))

    print(request.form['type'])
    print(request.form['price'])
    #TODO: Choose Headphones based off of these params

    return classification

def typeReccomend(data):
    if (data['type'] == 'On Ear'):
        return onEarRec(data)
    elif (data['type'] == 'Over Ear'):
        return overEarRec(data)
    else:
        return iemRec(data)

#dictionary must have 'type', 'class', 'sig' keys
def overEarRec(data):
    portClass = data['class']
    signature = data['sig']
    if (portClass == 'Portable'):
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"
    else: #(portClass == 'Not Portable')
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"

#dictionary must have 'type', 'backing', 'sig' keys
def onEarRec(data):
    backClass = data['backing']
    signature = data['sig']
    if (backClass == 'Open Back'):
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"
    else: #(backClass == 'Closed Back')
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"

#dictionary must have 'type', 'wear', 'sig' keys
def iemREC(data):
    wearClass = data['wear']
    signature = data['sig']
    if (wearClass == 'Straight Down'):
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"
    else: #(wearClass == 'Over Ear')
        if (signature == 'v_shaped'):
            return "amazonlink1"
        elif (signature == 'mid_forward'):
            return "amazonlink2"
        elif (signature == 'bass'):
            return "amazonlink3"
        else: #(signature == 'neutral')
            return "amazonlink4"





