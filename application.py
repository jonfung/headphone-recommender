import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import classify
import convert
import headphones

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

    data = request.form.to_dict()
    data['sig'] = classification

    return headphones.typeReccomend(data)


if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
