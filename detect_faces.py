# rldw 04/04/15
# https://github.com/rldw
#
# DESCRIPTION:
# walks through a given folder, detects faces on
# images inside, draws a rectangle around the faces
# and saves the image to the outdir with the filename
# x_filename, where x is the number of recognized faces
#
# USAGE:
# python detect_faces.py
# -c --cascadeXML	file for opencv pattern recognition algorithm
# -i --indir		folder with images to analyze
# -o --outdir		folder to save images to

import cv2, os, sys, argparse

# parse command line arguments
parser = argparse.ArgumentParser(description='walks through a given folder, detects faces on images inside, draws a rectangle around the faces and saves the image to the outdir with the filename x_filename, where x is the number of recognized faces')
parser.add_argument('-c','--cascadeXML', required=True,
	help='file for opencv pattern recognition algorithm')
parser.add_argument('-i','--indir', required=True,
	help='folder with images to analyze')
parser.add_argument('-o','--outdir', required=True,
	help='folder to save images to')
args = parser.parse_args()

def detectFace(img, outdir):
	image = cv2.imread(img)
	gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# detect faces in the image
	faces = faceCascade.detectMultiScale (
		gray,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize = (20, 20),
		flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)

	# draw green rectangle around face
	for (x,y,w,h) in faces:
		cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)

	numOfFaces = len(faces)
	imgname = str(numOfFaces) + "_" + img.split('/')[-1]
	filename = outdir + imgname

	# save image to filename
	cv2.imwrite(filename, image)
	return filename




outdir = args.outdir
if outdir[-1] != '/':
	outdir += '/'

if not os.path.exists(outdir):
	os.makedirs(outdir)

indir = args.indir
if indir[-1] != '/':
	indir += '/'


# path to cascade xml file
cascPath = args.cascadeXML

# create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

count = 0
for filename in os.listdir(indir):
	if filename[-3:] != 'jpg':
		continue

	path = indir + filename
	savedto = detectFace(path, outdir)
	print "saved image {0} to {1}".format(count, savedto)
	count += 1