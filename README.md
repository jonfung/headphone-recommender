# [headphone-recommender](jonfung.me/mp3-fft)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b89fc3565c5c4fdbaaf3ce579ef717d5)](https://www.codacy.com/app/drklee3/headphone-recommender?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jonfung/headphone-recommender&amp;utm_campaign=Badge_Grade)

Finds the perfect headphone with a matching sound signature for your favorite song.

## How it Works
First, the mp3 is converted to a .wav file, where it is run through a 4096-point welch's method. The resulting power spectral density(PSD) for the song is then analyzed for sound signature.

Below, we can see two examples.

Bass Heavy             |  S-shaped
:-------------------------:|:-------------------------:
![Runaway-Kanye](http://i.imgur.com/LwDQD92.png)  |  ![All Out of Love-Carpenters](http://i.imgur.com/ngHGA6e.png)

Notice how for [Runaway](https://youtu.be/Bm5iA4Zupek?t=60), a signifigant portion of the power spectrum lies in the lower end of the frequencies, resulting in a "bump" in the lower half of the PSD that tapers downward corresponding to the bassy undertones of the song.

However, for [All out of Love](https://youtu.be/JWdZEumNRmI?t=14), which is filled with vocals and higher frequencied guitar sounds, we notice the PSD to have a greater amount of frequencies lying in the high end (bump on end of the log scale). Combined with the bump in the lower freuqencies of the PSD, we determine the sound signature to be V-shaped.

By then integrating between frequency boundaries, we can quantify low, mid, and high values. Because Welch's method normalizes the PSD to satisfy Parseval's relation (total power in time domain is same as total power in frequency domain), we can comapre the low, mid, and high ratios to determine sound signature of the song.

After that, a few questions are asked about preferred headphone form factor and type, and a suitable pair of headphones can be reccomended!


## Usage
Currently hosted on heroku at link above. However, there is a song length restriction of 4:15 due to the RAM limitations of free hosting. If you would like to run this locally to analyze longer mp3 files:

Clone the repository.

    $ git clone https://github.com/jonfung/headphone-recommender.git
    $ cd flask-app-template
Create a virtualenv and activate.

    $ virtualenv env 
    $ source env/bin/activate
Install requirements.

    $ pip3 install -r requirements.txt
Install FFMPEG. Installation may vary for each system. For Ubuntu:

    $ sudo apt-get install ffmpeg
    
To remove song length restriction, set line 9 of `classify.py` to be:

  `SONG_DURATION_LIMITATION = True;`

Start the flask application:

	$ python3 application.py

Open localhost at browser:

	http://0.0.0.0:5000/
