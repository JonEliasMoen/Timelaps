import os
import Image
import math
import platform
import time
class getevopt(object):
	def __init__(self):
		if platform.system() == "Windows":
			import pygame.camera
			pygame.camera.init()
			clist = pygame.camera.list_cameras()
			
			if not clist:
				raise ValueError("Sorry, no cameras detected.")
			
			self.cam = pygame.camera.Camera(clist[0], (2304,1536), "YUYV") # define camera
	def capture(self, imagestring):
		import pygame.camera
		MyPlatform = platform.system()
		
		if MyPlatform == "Linux":
			execute("sudo fswebcam -q --jpeg 95 -d /dev/video0 -i 0 -r 2304x1536 --no-banner --no-timestamp %s"% imagestring) # -p YUYV, capture image
		
		elif MyPlatform == "Windows":
			#use pygame to capture image
			self.cam.start()
			surface = pygame.Surface((2304,1536))
			image = self.cam.get_image(surface)
			pygame.image.save(image, imagestring)
			self.cam.stop()
			
		time.sleep(0.25)
	def GetB(self, imagestring):
		image = Image.open(imagestring)
		pix = image.load()
		sumb = 0
		for x in range(image.size[0]):
			for y in range(image.size[1]):
				b = pix[x,y][0]*0.2126 + pix[x,y][1]*0.7152 + pix[x,y][2]*0.0722
				sumb += b
		bpre = sumb/(image.size[0]*image.size[1])
		return bpre
	def main(self):
		# take image with set ev
		os.system("v4l2-ctl --set-ctrl exposure_absolute=1000")
		
		timestart = time.time()
		self.capture("ev.jpg")
		timeused = time.time()-timestart
		
		bpre = self.GetB()
		
		evopt = 1000 + math.log(bpre,2) - math.log(2500/2, 2) # 2500/2 is just temporary
		
		print(evopt)
		return evopt
	
clas = getevopt()

sumb = 0
loopcount = 0
avgb = 0
while True:
	loopcount += 1
	#clas.capture("B opt images/%s.jpg"% str(loopcount))
	sumb += clas.GetB("B opt images/%s.jpg"% str(loopcount))
	avgb = sumb/loopcount
	print(avgb)
	
# x = open("evopt.txt")
# x.write(str(evopt))
# x.close()

