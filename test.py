import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename
import classify
import convert

#os.system('rm bob.mp3')

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)

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