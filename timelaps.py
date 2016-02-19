import os
import time
import platform


MyPlatform = platform.system() # current operating system

def execute(what): # commandline execute
	os.system(what)

class camera(object):
	def __init__(self):
		
		global MyPlatform
		if MyPlatform == "Linux":
			folder = os.listdir("/dev")
			if "video1" or "video0" in folder:
				print "camera connected"
			else:
				print "please connect a camera, and run the script again"
				exit()
		else:
			import pygame.camera
			pygame.camera.init()
			clist = pygame.camera.list_cameras()
			
			if not clist:
				raise ValueError("Sorry, no cameras detected.")
			
			self.cam = pygame.camera.Camera(clist[0], (2304,1536), "YUYV") # define camera
			
	def capture(self, imagestring, loopcount):
		import pygame.camera
		global MyPlatform #platform name
		print "capturing %s"% imagestring
		
		if MyPlatform == "Linux":
			execute("sudo fswebcam -q --jpeg 95 -d /dev/video0 -i 0 -r 2304x1536 --no-banner --no-timestamp %s"% imagestring) # -p YUYV, capture image
		
		elif MyPlatform == "Windows":
			#use pygame to capture image
			self.cam.start()
			
			pygame.image.save(self.cam.get_image(), imagestring)
			self.cam.stop()
			
		self.writetimestamp(imagestring, loopcount)
		time.sleep(0.25)
	def writetimestamp(self,image, a):
		date = time.strftime("%a %d.%m.%Y %H:%M:%S") # get current time, in this form day daynumber.month.year time:minute:second
		if MyPlatform == "Linux":
			import Image
			import ImageFont
			import ImageDraw
			import ImageStat
			
			font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 20) # get font
			
			print "writing timestamp on image: " + date
			
			im = Image.open( image )
			

			canvas = ImageDraw.Draw( im )
			canvas.rectangle( [(0,0), (280,40)] , fill=(0,0,0) )
			canvas.text( (10,10), date, (255,255,255), font=font)

			im.save(image)
		else:
			x = open("timestamp.txt", "a")
			x.write(date + "=-=" + str(a)+"\n")
			x.close()
class SettingFunc(object):
	def getsetting(self, filename):
		x = open("settings/%s"% filename)
		line = x.readline()
		while line != '':
			if list(line)[0] != '\n':
				#print list(line)
				self.setting(line)
			else:
				print "invalid setting"
			line = x.readline()
			
	def checksetting(self, settingsfolder, setting):
		x = open(settingsfolder + setting)
		lines = x.readlines()
		print
		print "setting: " + setting
		for i in lines:
			print i[0: len(i)-2]
		x.close()
	
	
	def setting(self, sett):
		#remove \n
		lastchar = sett[len(sett)-1 : len(sett)]
		if lastchar == '\n':
			sett = sett[0:len(sett)-1]
		
		print "setting setting:%s "% sett
		
		if sett != " " or "\n" or '\n' or '': 
			os.system("v4l2-ctl --set-ctrl %s"% sett) # sett the setting
class Nxt(object):
	def PortToMethod(port):
		meth = "a"
		if port.upper() == "A":
			meth = nxt.motor.PORT_A
		elif port.upper() == "B":
			meth = nxt.motor.PORT_B
		elif port.upper() == "C":
			meth = nxt.motor.PORT_C
		return meth
	def __init__(self):
		import nxt.locator
		import nxt.motor
		sock = nxt.locator.find_one_brick()
		self.brick = sock.connect()
		
		self.Motor_a = nxt.motor.Motor(self.brick, PortToMethod(config["Motor1"]) )
		self.Motor_b = nxt.motor.Motor(self.brick, PortToMethod(config["Motor2"]) )
		
		self.loopcount = 0
	def main(self,config): # called every minute, uses TurnInverval for when to execute
		self.loopcount += 1
		if loopcount == 1:
			self.left = config["TurnInterval"]-1
		else:
			self.left -= 1
		if self.left == 0:
			self.left = config["TurnInterval"]
			self.Motor_a.update(config["TurnPower"], config["TurnAngle"], True)
			self.Motor_
def move(imagestring, numb):
	print "moving to webserver"
	execute("sudo cp %s /var/www/webcam/now/webcam%s.jpg"% (imagestring,str(numb)))
	

def movecurrent(current): #autochange
	execute("sudo mv settings settings_%s"% current.upper() )

def usersettings():
	global currentsetting, MyPlatform
	# Autochange, SinglePic, CurrentSettingName, SinglePicCaptureFolder, AutoRotate, Motor1, Motor2, TurnInterval, TurnPower
	config = {"AutoChange" : False} # config dictionary
	config["SinglePic"] = raw_input("Single image?, (1=yes, 0=no):")
	
	if config["SinglePic"] == "0":
		config["SinglePic"] = False
		
		config["AutoChange"] = raw_input("auto change camera settings (1=yes, 0=no): ")
		if config["AutoChange"] == "1":
			config["AutoChange"] = True
			config["CurrentSettingName"] = raw_input("current setting name: ")
		else:
			config["AutoChange"] = False
	
	elif config["SinglePic"] == "1":
		config["SinglePic"] = True
		
		config["SinglePicCaptureFolder"] = raw_input("folder to capture to (1,2,3):")
	
	#nxt
	config["AutoRotate"] = raw_input("AutoRotate using nxt?: (1=yes 0=no):")
	if config["AutoRotate"] == "0":
		config["AutoRotate"] = False
	if config["AutoRotate"] == "1":
		config["AutoRotate"] = True
		
		motors = raw_input("Nxt Motors? list two (a b c): ")
		config["Motor1"] = motors[0]
		config["Motor2"] = motors[1]
	
		config["TurnInterval"] = int(raw_input("Turn every x minute: "))
		config["TurnPower"] = int(raw_input("With how much power (1-100): "))
		config["TurnAngle"] = int(raw_input("How many high angle of turn every update: "))
		
	return config

config = usersettings()
#get picture number
x = open("number.txt")
a = int(x.readline())
x.close()

#class init
SettingClass = SettingFunc()
camera = camera()
camera.__init__()

if MyPlatform == "Linux": #folder name fixes
	prefix = "./"
	folder = "selbulantimelapsv2"
	if not os.path.exists(prefix+folder):
		os.system("mkdir %s"% prefix+folder)


	settingsfolder = "./settings/"
	files = os.listdir(settingsfolder[0:len(settingsfolder)-1])
	print "settings: " + str(files)

	for sett in files:
		SettingClass.checksetting(settingsfolder, sett)
else:
	prefix = os.getcwd()[2:len( os.getcwd() )]
	folder = "\selbulantimelapsv2"
	os.system("mkdir %s"% prefix+folder)

#setting("focus_auto=1")



while True:
	start = time.time()
	a = a+1
	
	x = open("number.txt", "w")
	x.write(str(a))
	x.close()
	
	#get setting filenames
	loopcount  = 0
	if MyPlatform == "Linux":
		
		if config["SinglePic"] == False:
			SettingClass.setting("exposure_auto=3")
			SettingClass.setting("exposure_auto_priority=1")
			for i in files:
				imagestring = prefix+folder+"/%s/%s.jpg"% (str(i), a)
				print "imagestring: %s"% imagestring

				SettingClass.getsetting(str(i)) #get and set settings
				camera.capture(imagestring, a) # capture image
				move(imagestring, i) # copy to webserver
				print
		
		else:
			imagestring = prefix+folder+"/%s/%s.jpg"% (config["SinglePicCaptureFolder"], a)
		
		
			SettingClass.setting("exposure_auto=1")
			SettingClass.setting("exposure_auto_priority=0")
			
			camera.capture(imagestring, a) # capture image
			move(imagestring, config["SinglePicCaptureFolder"]) # copy to webserver
		
		print
		
		#auto change settings
		if config["AutoChange"] == True:
			targets = { (18,0) : "natt", (6,0) : "dag" }
			time = ( int(time.strftime("%H")),int(time.strftime("%M")))
			if time in targets:
				targetsetting = targets[time]
				movecurrent( currentsetting )
				for type in targets.keys():
					if targetsetting == type:
						execute("sudo mv settings_%s settings"% type.upper() )
	else:
		imagestring = prefix+folder+"/%s/%s.jpg"% (str(2), a)
		
		camera.capture(imagestring, a) # capture image
	
	end = time.time()
	timeused = end-start
	print "time used: %s	time left to new round: %s	secound of film: %s"% (str(timeused), str(60-timeused), float(a/24.0)) 
	print
	print
	time.sleep(60-(end-start))
	