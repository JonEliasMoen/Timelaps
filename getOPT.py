import os
import imaging
import math
class getevopt(object):
	def main():
		# take image with set ev
		os.system("v4l2-ctl --set-ctrl exposure_absolute=1000")
		ös.system("sudo fswebcam -q --jpeg 95 -d /dev/video0 -i 0 -r 2304x1536 --no-banner --no-timestamp ev.jpg")
		
		image = Image.open("ev.jpg")
		pix = image.load()
		
		sumb = 0
		for x in image.size[0]:
			for y in image.size[1]:
				b = pix[x,y][0]*0.2126 + pix[x,y][1]*0.7152 + pix[x,y][2]*0.0722
				sumb += b
		bpre = sumb/(image.size[0]*image.size[1])
		evopt = 1000 + math.log(bpre,2)
		
		print(evopt)
		return evopt

clas = getevopt()
clas.main()
