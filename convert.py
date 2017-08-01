import ffmpy
import os

CONTAINING_FOLDER = "uploads"

def convert(infile, outfile):
	inpath = os.path.join(CONTAINING_FOLDER, infile)
	outpath = os.path.join(CONTAINING_FOLDER, outfile)
	ff = ffmpy.FFmpeg(
		inputs = {inpath: None},
		outputs = {outpath: '-y'}
	)
	ff.run()
	os.remove(inpath)