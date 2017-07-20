from flask import jsonify

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
                cans = {
                    150: "Beyerdynamic DT990 Pro",
                    200: "Beyerdynamic DT990 Premium",
                    250: "Philips Fidelio X2",
                }
                return jsonify(signature = signature, headphones = cans)                
            elif (signature == 'Mid Forward'):
                cans = {
                    30: "Superlux HD681(b)",
                    75: "Philips SHP9500",
                    80: "Audio Technica ATH AD500X",
                    150: "Audio Technica ATH AD900X",
                    200: "AKG K702 and Q701",
                    250: "Beyerdynamic DT880 Premium",
                    550: "Audio Technica ATH AD2000X",
                }
                return jsonify(signature = signature, headphones = cans)
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
                cans = {
                    150: "Beyerdynamic DT770 Studio",
                    175: "Shure SRH 840",
                    250: "Cascadia Audio TALOS",
                    400: "Fostex TH-X00",
                    550: "Shure SRH1540",
                    1200: "Fostex TH900",
                }
                return jsonify(signature = signature, headphones = cans)                
            elif (signature == 'Mid Forward'):
                cans = {
                    160: "Fostex T50RP Mk3",
                    175: "Audio Technica ATH A900X",
                    300: "Beyerdynamic T70p",
                    400: "Audio Technica ATH A1000Z",
                }
                return jsonify(signature = signature, headphones = cans)
            elif (signature == 'Bass'):
                cans = {
                    20: "Sennheiser HD202",
                    150: "Fostex T20RP Mk3",
                    175: "AKG K553 PRO",
                    480: "ZMF Vibro MkII",
                }
                return jsonify(signature = signature, headphones = cans)
            else: #(signature == 'Neutral')
                cans = {
                    90: "NVX XPT 100",
                    110: "Brainwavz HM5",
                }
                return jsonify(signature = signature, headphones = cans)

#dictionary must have 'type', 'backing', 'sig' keys
def onEarRec(data):
    backClass = data['backing']
    signature = data['sig']
    if (backClass == 'Open Back'):
        cans = {
            20: "Koss KSC75",
            50: "Koss Porta Pro",
            70: "Sennheiser HD239",
        }
        return jsonify(signature = signature, headphones = cans)
    else: #(backClass == 'Closed Back')
        if (signature == 'V Shaped'):
            cans = {
                55: "Beyerdynamic DTX350M",
                85: "Beyerdynamic DTX501P",
                200: "Beyerdynamic T51P",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Mid Forward'):
            cans = {
                475: "Audeze Sine",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Bass'):
            cans = {
                90: "Sennheiser Urbanite On Ear",
                120: "Beats Solo 2",
                175: "V-Moda XS",
            }
            return jsonify(signature = signature, headphones = cans)
        else: #(signature == 'Neutral')
            cans = {
                75: "Noontec Zoro HDII",
                150: "Sennheiser HD25",
                175: "Beyerdynamic DT1350",
                250: "Sennheiser Amperior",
            }
            return jsonify(signature = signature, headphones = cans)

#dictionary must have 'type', 'fit', 'sig' keys
def iemRec(data):
    wearClass = data['fit']
    signature = data['sig']
    if (wearClass == 'Over Ear'):
        if (signature == 'V Shaped'):
            cans = {
                55: "TFZ Series 3",
                75: "Vsonic VSD5",
                100: "RHA MA750",
                275: "Fidue A83",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Mid Forward'):
            cans = {
                40: "Vsonic VSD2S",
                120: "Hippo Pro One",
                175: "Shure SE315",
                300: "Audio Technica ATH IM03",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Bass'):
            cans = {
                12: "KZ ATE",
                40: "Vsonic VSD3S",
                50: "Audio Technica ATH IM50",
                80: "TFZ Series 5",
                100: "Shure SE215",
                185: "RHA T10(i)",
                280: "Logitech UE900s",
                300: "Sennheiser IE80",
                550: "Westone W50",
            }
            return jsonify(signature = signature, headphones = cans)
        else: #(signature == 'Neutral')
            cans = {
                45: "MEE Audio M6PRO",
                100: "VSonic GR07",
                200: "MEE Audio Pinnacle (P1)",
                200: "Audio Technica ATH IM02",
                300: "Shure SE425",
                375: "Westone W30",
                650: "DITA The Answer",
            }
            return jsonify(signature = signature, headphones = cans)
    else: #(wearClass == 'Straight Down')
        if (signature == 'V Shaped'):
            cans = {
                10: "Philips SHE3595",
                25: "Xiaomi Hybrid",
                80: "One More Triple Driver",
                100: "Sennheiser Momentum In Ear",
                180: "Dunu DN-1000",
                275: "Dunu DN-2000",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Mid Forward'):
            cans = {
                75: "FiiO EX1",
                130: "Dunu Titan 3",
                300: "Dunu DN-2000J",
            }
            return jsonify(signature = signature, headphones = cans)
        elif (signature == 'Bass'):
            cans = {
                30: "Vsonic GR02/BE",
                35: "Soundmagic E10",
                50: "Soundmagic E50S",
                85: "Yamaha EPH-100SL",
                175: "JVC HA-FX750",
            }
            return jsonify(signature = signature, headphones = cans)
        else: #(signature == 'Neutral')
            cans = {
                20: "Brainwavz Delta",
                30: "Zero Audio Carbo Tenore",
                60: "Fidue A63",
                80: "Hifiman RE400",
                95: "Philips Fidelio S2",
                120: "Etymotic Resarch HF5",
                350: "Etymotic Research ER4SR",
            }
            return jsonify(signature = signature, headphones = cans)
