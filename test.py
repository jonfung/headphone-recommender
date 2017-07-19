import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.utils import secure_filename
import classify
import convert

#os.system('rm bob.mp3')

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/test')
def test():
	return url_for('show_user_profile',username = 'Frank', age = 12)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         mp3name = secure_filename(f.filename)
#         f.save(os.path.join(UPLOAD_FOLDER, mp3name))
#         wavname = mp3name[:len(mp3name) - 4] + ".wav"
#         convert.convert(mp3name, wavname)

#         classification = classify.runClassify(wavname)
#         os.remove(os.path.join(UPLOAD_FOLDER, wavname))
#     return classification


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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


