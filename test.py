import os
from flask import Flask, request, redirect, flash, send_from_directory, jsonify
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

    data = request.form.to_dict()
    data['sig'] = classification
    #TODO: Choose Headphones based off of these params
    # print(typeReccomend(data))
    return typeReccomend(data)

def typeReccomend(data):
    if (data['type'] == 'On Ear'):
        return onEarRec(data)
    elif (data['type'] == 'Over Ear'):
        return overEarRec(data)
    else: #(must be In Ear Monitor)
        return iemRec(data)

#dictionary must have 'type', 'portability', 'sig' keys
def overEarRec(data):

    portClass = data['portability']
    signature = data['sig']
    if (portClass == 'Portable'):
        if (signature == 'V Shaped'):
            cans = {
                150: "Audio Technica ATH M50X",
                150: "Sony MDR 100 AAP",
                180: "Soundmagic HP150",
                300: "Ultrasone PRO900 S-Logic",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Mid Forward'):
            cans = {
                25: "Incipio F38 Forte",
                100: "KRK KNS6400",
                230: "Audio Technica ATH MAR7",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Bass'):
            cans = {
                20: "TASCAM TH02",
                60: "Creative Aurvana L!ve",
                120: "Sennheiser Urbanite",
                180: "Beyerdynamic COP",
                250: "Sennheiser Momentum 2",
                250: "V-Moda M100",
                300: "Meze 99",
                400: "Oppo PM3",
            }
            return jsonify(signature = signature, headphones = cans)

        else: #(signature == 'Neutral')
            cans = {
                25: "Monoprice 8323",
                90: "Audio Technica ATH M40X",
                185: "AKG K545",
                250: "NAD Viso HP50",
                275: "PSB M4U1",
            }
            return jsonify(signature = signature, headphones = cans)

    else: #(portClass == 'Not Portable')
        backClass = data['backing']
        if (backClass == 'Open Back'):
            if (signature == 'V Shaped'):
                return "amazonlink1"
            elif (signature == 'Mid Forward'):
                return "amazonlink2"
            elif (signature == 'Bass'):
                cans = {
                    40: "Superlux EVO",
                    100: "Sennheiser HD558",
                    200: "AKG K7XX",
                    400: "Sennheiser HD650",
                    550: "Audioquest Nighthawk",
                }
                return jsonify(signature = signature, headphones = cans)
            else: #(signature == 'Neutral')
                cans = {
                    100: "AKG K240 Studio",
                    150: "AKG K612 Pro",
                    150: "Sennheiser HD598",
                    300: "Sennheiser HD600",
                    350: "Audio Technica ATH R70X",
                    450: "Hifiman HE400i",
                }
            return jsonify(signature = signature, headphones = cans)

        else: #(backClass == 'Closed Back')
            if (signature == 'V Shaped'):
                return "amazonlink1"
            elif (signature == 'Mid Forward'):
                return "amazonlink2"
            elif (signature == 'Bass'):
                return "amazonlink3"
            else: #(signature == 'Neutral')
                return "amazonlink4"

#dictionary must have 'type', 'backing', 'sig' keys
def onEarRec(data):
    backClass = data['backing']
    signature = data['sig']
    if (backClass == 'Open Back'):
        if (signature == 'V Shaped'):
            return "amazonlink1"
        elif (signature == 'Mid Forward'):
            return "amazonlink2"
        elif (signature == 'Bass'):
            return "amazonlink3"
        else: #(signature == 'Neutral')
            return "amazonlink4"
    else: #(backClass == 'Closed Back')
        if (signature == 'V Shaped'):
            return "amazonlink1"
        elif (signature == 'Mid Forward'):
            return "amazonlink2"
        elif (signature == 'Bass'):
            return "amazonlink3"
        else: #(signature == 'Neutral')
            return "amazonlink4"

#dictionary must have 'type', 'fit', 'sig' keys
def iemREC(data):
    wearClass = data['fit']
    signature = data['sig']
    if (wearClass == 'Straight Down'):
        if (signature == 'V Shaped'):
            return "amazonlink1"
        elif (signature == 'Mid Forward'):
            return "amazonlink2"
        elif (signature == 'Bass'):
            return "amazonlink3"
        else: #(signature == 'Neutral')
            return "amazonlink4"
    else: #(wearClass == 'Over Ear')
        if (signature == 'V Shaped'):
            return "amazonlink1"
        elif (signature == 'Mid Forward'):
            return "amazonlink2"
        elif (signature == 'Bass'):
            return "amazonlink3"
        else: #(signature == 'Neutral')
            return "amazonlink4"





