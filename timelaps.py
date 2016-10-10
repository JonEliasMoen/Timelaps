import os
import time
import platform
import math


MyPlatform = platform.system() # current operating system
timestampPath = "timestamp.txt"
numberPath = "number.txt"
settingsfolder = "./settings/" # linux
def execute(what): # commandline execute
	os.system(what)

class camera(object):
	def __init__(self):
		global MyPlatform
		if MyPlatform == "Linux":
			folder = os.listdir("/dev")
			if "video1" or "video0" in folder:
				print("camera connected")
			else:
				print("please connect a camera, and run the script again")
				exit()
		else:
			import pygame.camera
			pygame.camera.init()
			clist = pygame.camera.list_cameras()
			if len(clist)>1:
				print "there is more than one camera connected, using the first one detected"
				
			#find the resoulution that works with the camera
			loopcount = -1
			sizes = [(1080,720), (2304,1536), (640,480), (320,240),(800,600)]
			going = True
			while going:
				going = False
				try:
					self.size = sizes[loopcount]
					self.cam = pygame.camera.Camera(clist[0], self.size) # define camera
				except:
					loopcount += 1
					going = True
			print "set resolution to: " + str(self.size)
	def capture(self, imagestring, loopcount, writetime):
		import pygame.camera
		global MyPlatform #platform name
		print("capturing %s"% imagestring)
		
		timestart = time.time()
		if MyPlatform == "Linux":
			execute("sudo fswebcam -q --jpeg 95 -d /dev/video0 -i 0 -r 1080x720 --no-banner --no-timestamp %s"% imagestring) # -p YUYV, capture image
		
		elif MyPlatform == "Windows":
			import pygame.camera
			self.cam.start()
			surface = pygame.Surface(self.size)
			image = self.cam.get_image(surface)
			pygame.image.save(image, imagestring)
			self.cam.stop()
		
		timeused = time.time()-timestart

		if writetime == "no":
			self.logtimestamp(loopcount)
		else:
			self.writetimestamp(imagestring, loopcount)
		time.sleep(0.25)
		return timeused
	def writetimestamp(self,image, a):
		global timestampPath
		date = time.strftime("%a %d.%m.%Y %H:%M:%S") # get current time, in this form day daynumber.month.year time:minute:second
		failed = False
		try:
			import Image
			import ImageDraw
			import ImageFont
			import ImageStat
		except:
			self.logtimestamp(a)
			failed = True
		if failed == False:
			ont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 20) # get font
			
			print("writing timestamp on image: " + date)
			
			im = Image.open( image ) # problems with reading the imagestring, it is formated wrongly
			

			canvas = ImageDraw.Draw( im )
			canvas.rectangle( [(0,0), (280,40)] , fill=(0,0,0) )
			canvas.text( (10,10), date, (255,255,255), font=font)

			im.save(image)
	def logtimestamp(self, a):
		global timestampPath
		date = time.strftime("%a %d.%m.%Y %H:%M:%S") # get current time, in this form day daynumber.month.year time:minute:second

		x = open(timestampPath, "a")
		x.write(date + "=-=" + str(a)+"\n")
		x.close()
class SettingFunc(object):
	def getsetting(self, filename):
		x = open("settings/%s"% filename)
		line = x.readline()
		while line != '':
			if list(line)[0] != '\n': # if not empty enter
				#print list(line)
				self.setting(line) # use the setting
			else:
				print("invalid setting: " + line)
			line = x.readline()
			
	def checksetting(self, settingsfolder, setting):
		x = open(settingsfolder + setting)
		lines = x.readlines()
		print()
		print("setting: " + setting)
		for i in lines:
			print(i[0: len(i)-2])
		x.close()
	
	
	def setting(self, sett):
		#remove \n
		lastchar = sett[len(sett)-1 : len(sett)]
		if lastchar == '\n':
			sett = sett[0:len(sett)-1]
		
		print("setting setting:%s "% sett)
		
		if sett != " " or "\n" or '\n' or '': 
			os.system("v4l2-ctl --set-ctrl %s"% sett) # sett the setting
class Nxt(object): # out of function
	def __init__(self):
		import nxt.locator
		import nxt.motor
		sock = nxt.locator.find_one_brick()
		self.brick = sock.connect()
		
		self.Motor = nxt.motor.Motor(self.brick, PORT_ALL)
		
		self.loopcount = 0
	def main(self,config): # called every minute, uses TurnInverval for when to execute
		self.loopcount += 1
		if loopcount == 1:
			self.left = config["TurnInterval"]-1 # minus one because it counts current round
		else:
			self.left -= 1
			
		if self.left == 0:
			self.left = config["TurnInterval"]
			self.Motor.update(config["TurnPower"], config["TurnAngle"], True)
class server(object):
	def server(self):
		self.socket.listen(5)
		self.client, addr = s.accept()
	
	def ServerUpdate(self, message):
		c.send(message)
	
	def main(config):
		import socket
		self.socket = socket.socket()
		if config["SocketCapSyncType"] == "server":
			host = config["InternetProtocolAdress"]
			self.socket.bind((host,123))
			server(self)
		else:
			host = socket.gethostname()
			self.socket.bind((host,123))
			client(self)
			
def move(imagestring, numb):
	print("moving to webserver")
	execute("sudo cp %s /var/www/webcam/now/webcam%s.jpg"% (imagestring,str(numb)))
	

def movecurrent(current): #autochange
	execute("sudo mv settings settings_%s"% current.upper() )
def WriteLoopcunt(loopcount): # write loopcount to text file
	global numberPath
	x = open(numberPath, "w")
	x.write(str(loopcount))
	x.close()
class usersettings(object):
	def SocketCapSync(self):
		global MyPlatform
		if self.config["SocketCapSync"] == "yes":
			self.config["SocketCapSyncType"] = input("server or client?:")
			self.config["InternetProtocolAdress"] = input("ip? (if server then my ip, if client then their ip):")
		else:
			self.config["SocketCapSyncType"] = None
			self.config["InternetProtocolAdress"] = None
	def SinglePic(self):
		if self.config["SinglePic"] == "no":
			self.config["AutoChange"] = input("auto change camera settings (1=yes, 0=no): ")
			self.config["AutoChange"] = self.NumbToBool(self.config["AutoChange"])
			
			if self.config["AutoChange"] == True:
				self.config["CurrentSettingName"] = input("current setting name: ")
			else:
				self.config["AutoChange"] = False
			
			if MyPlatform == "Linux":
				self.config["ExAlgo"] = input("Use homemade exposure algorithm? (yes=1, no=0: ")
				self.config["ExAlgo"] = self.NumbToBool(self.config["ExAlgo"])
		else:
			self.config["SinglePicCaptureFolder"] = raw_input("folder to capture to (1,2,3):")
			self.config["AutoChange"] = None
			self.config["CurrentSettingName"] = None
			self.config["ExAlgo"] = None
	def Nxt(self):
		if self.config["AutoRotate"] == "yes":
			self.config["TurnInterval"] = int(input("Turn every x minute: "))
			self.config["TurnPower"] = int(input("With how much power (1-100): "))
			self.config["TurnAngle"] = int(input("How many high angle of turn every update: "))
		else:
			self.config["TurnInterval"] = None
			self.config["TurnPower"] = None
			self.config["TurnAngle"] = None
	def main(self):
		global currentsetting, MyPlatform
		# Autochange, SinglePic, CurrentSettingName, SinglePicCaptureFolder, AutoRotate, TurnInterval, TurnPower
		self.config = {"AutoChange" : False} # config dictionary
		
		self.config["SocketCapSync"] = raw_input("Network Camera Syncing?: (yes or no):")
		self.SocketCapSync()
		
		self.config["SinglePic"] = raw_input("Single image?, (yes or no):")
		self.SinglePic()

		self.config["AutoRotate"] = raw_input("AutoRotate using nxt?: (yes or no):")
		self.Nxt()
		
		self.config["WriteTimestamp"] = raw_input("Write timestamp on image? (yes or no): ")
		
		return self.config
clas = usersettings()
config = clas.main()


#get picture number
x = open("number.txt")
loopcount = int(x.readline())
x.close()

#class init
SettingClass = SettingFunc()
camera = camera()
#server = server()

if MyPlatform == "Linux": #folder name fixes
	prefix = "./"
	folder = "selbulantimelapsv2"
	if not os.path.exists(prefix+folder):
		os.system("mkdir %s"% prefix+folder)


	SettingsFiles = os.listdir(settingsfolder)
	print("SettingFiles: " + str(SettingsFiles))

	for sett in SettingsFiles:
		SettingClass.checksetting(settingsfolder, sett) #just printing them, so that the user can spot mistakes
		#wait for input
		raw_input("continue?, (if not press Ctrl + C)")
else:
	a = "\s"
	prefix = os.getcwd()[2:len( os.getcwd() )]
	folder = "\selbulantimelapsv2"
	os.system("mkdir %s"% prefix+folder)
#setting("focus_auto=1")

while True:
	timestart = time.time()
	
	loopcount += 1
	WriteLoopcunt(loopcount) # write to txt
	
	if MyPlatform == "Linux":
		
		if config["SinglePic"] == "no": # we are not doing singlepictures
		
			SettingClass.setting("exposure_auto=3") 
			SettingClass.setting("exposure_auto_priority=1")
			for SettFile in SettingFiles:
				imagestring = prefix+folder+"/%s/%s.jpg"% (str(SettFile), loopcount)
				print("imagestring: %s"% imagestring)

				SettingClass.getsetting(str(SettFile)) #get and set settings
				CaptureTime = camera.capture(imagestring, loopcount) # capture image
				move(imagestring, SettFile) # copy to webserver
				print()
		
		else: # singlepictures for linux
			imagestring = prefix+folder+"/%s/%s.jpg"% (config["SinglePicCaptureFolder"], loopcount)

			if config["ExAlgo"] == True:
				SettingClass.setting("exposure_auto=0")
				
				focuslen = 5 # meter
				fnumber = focuslen/0.008
				exposuredur = 10 #second
				ev = math.log( (math.pow(fnumber,2)/exposuretime), 2)
				
				SettingClass.setting("exposure_absolute=" + str(ev))
			else:
				SettingClass.setting("exposure_auto=1")
				SettingClass.setting("exposure_auto_priority=1")
			
			CaptureTime = camera.capture(imagestring, loopcount) # capture image
			move(imagestring, config["SinglePicCaptureFolder"]) # copy to webserver
		
		print()
		
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
	else: # windows just capture
		imagestring = prefix+folder+"\%s\%s.jpg"% (config["SinglePicCaptureFolder"], loopcount)
		
		camera.capture(imagestring, loopcount, config["WriteTimestamp"]) # capture image
		
	#wait
	timeused = time.time()-timestart
	print("time used: %s	time left to new round: %s	secound of film: %s"% (str(timeused), str(60-timeused), float(loopcount/24.0)) )
	print
	print
	time.sleep(60-timeused)
	
