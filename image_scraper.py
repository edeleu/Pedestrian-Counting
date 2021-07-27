import requests, time, os

#Dictionary of Camera Names and Corresponding URLs
urls={
	"6at34": "https://511ny.org/map/Cctv/4616423--17", 
	"5at23" :"https://511ny.org/map/Cctv/4616415--17",
	"5at42" : "https://511ny.org/map/Cctv/4616417--17",
	"6at49/50" :"https://511ny.org/map/Cctv/4616433--17",
	"5at49" :"https://511ny.org/map/Cctv/4616418--17",
	#"CameraName":"Camera URL"
} 

path = os.path.dirname(__file__) #Current File Path
ctr=1 #Counting Variable

def SaveImage(): #Image Saving Function
	global ctr
	for url in urls: #Loop over all cameras
		#Retrieve current time and date as string
		timestr = time.strftime("%Y-%m-%d__%H-%M") 
		
		#Create Filename 
		Name=url+"_"+timestr+".jpeg"
		dir=os.path.join(path,url)
		FinalPath=os.path.join(dir,Name)
		#Naming scheme: workingDir/CamName/CamName_YYYY-MM-DD__HR-MIN

		r = requests.get(urls[url]) #Open Image URL from current camera

		try: #Writes image file if no errors occur
			with open(FinalPath, "wb") as f:
				f.write(r.content)
		except: #Create folder for the current camera if it's missing
			if not os.path.exists(dir): os.mkdir(dir)
		print("iters: "+str(ctr))
		ctr+=1
	print("Waiting for 55 seconds....")
	time.sleep(60) 
	#Waits for one minute after images from each camera have been saved

try:
	while True: #Loop over SaveImage function
		SaveImage()
except KeyboardInterrupt: #Exit program if CTRL+C is pressed
	print("Exiting...")
	pass




