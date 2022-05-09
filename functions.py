import pysftp
import paramiko
import glob
import shutil
import os
import getpass
import time

def clearConsole():
	command = 'clear'
	if os.name in ('nt', 'dos'):  #if windows use cls
		command = 'cls'
	os.system(command)

def about():
	clearConsole()
	print("""
Zip file uploader

Maintainer: X Y; X.Y@Z.com

More in the readme_2.md file

Version 1.21

Enter to continue
	""")
	input()

def menu():
	clearConsole()
	print('''
--------------Menu--------------
	1 - Upload zips
	7 - Settings
	8 - Show this menu
	9 - About
	0 - Exit
--------------------------------
	''')
	return int(input('What do you want to do?\n'))

def upload(config):
	clearConsole()
	numInt = 0 #file count
	# numStr = '00' #same but in string and with 0 at the beginning (if numInt < 10)

	if numInt == 0:
		#check if password is provided in config.ini if so assign it to pass
		if len(config['server']['pass']) == 0:
			pas = getpass.getpass('Please type your password: ')
		else:
			pas = config['server']['pass']
		clearConsole()

	#loop through all files in waiting/
	#main loop; move first file to tmp/, rename it (remove counter e.g. 01_), upload file, then move it to uploaded/ and add counter 001_
	while True:
		#check if uploaded/ folder reached the limit - 999 zips
		if (len(glob.glob('**/uploaded/' + '*_*.zip', recursive = True))  >= 998):
			print("Clear folder: uploaded/")
			input("Enter to continue")
			break

		#if waiting is empty wait some time and check again
		if (len(glob.glob('**/waiting/' + '*_*.zip', recursive = True)) == 0):
			clearConsole()
			emptyT = int(config['server']['emptyTime']) * 60
			for i in range(emptyT,0,-1):
				clearConsole()
				print('Fodler waiting/ is empty.')
				print('Another check after: ' + str(i // 60) + 'm ' + str(i % 60) + 's')
				time.sleep(1)
			continue

		#Script will wait 10 seconds when it detects a new file at the beginning of the queue (with a name that starts with '01_'). Without it, script was crashing sometimes with message:
		#2022-05-06 14:26:18,001 ERROR __main__ [Errno 13] Permission denied: 'waiting\\01_xxx.zip'
		#I believe that windows was blocking access to a file while it was copied to the waiting/ directory by user
		#Script at the same time was trying to move it to tmp/. Now script will wait 10s. It will give some time to finish copying and will allow Windows to unlock the file
		if (glob.glob('**/waiting/' + '??_*.zip', recursive = True)[0][8:10]) =='01':
			for i in range(10,0,-1):
				clearConsole()
				print('New file detected, processing ...')
				print('Upload afer: ' + str(i // 60) + 'm ' + str(i % 60) + 's')
				time.sleep(1)

		numInt += 1
		if numInt < 10:
			numStr = '0' + str(numInt)
		else:
			numStr = str(numInt)
		
		#create list of zips in waiting/; list is sorted by names
		fileList = sorted( filter( os.path.isfile, glob.glob('**/waiting/' + '??_*.zip', recursive = True))) #returns sorted list of files
		targetFile = 'tmp/' + fileList[0][11:] #create path to tmp/
		#of course this can be done without tmp folder but I didn't want any files to flash there when user will be adding new files to waiting/, changing names etc. This could be confusing for user, and lead to missclicks etc.
		shutil.move(fileList[0], targetFile) #move file waiting/01_something.zip -> tmp/something.zip

		cnopts = pysftp.CnOpts()
		cnopts.hostkeys.load('key.txt.')


		#upload zip from tmp/
		clearConsole()
		print('Uploading file ...')
		with pysftp.Connection(host = config['server']['host'], username = config['server']['user'], port = int(config['server']['port']), password = pas, cnopts=cnopts) as sftp:
			with sftp.cd(config['server']['zipDestination']):
				sftp.put(targetFile)    #upload file
		
		#move and rename uploaded file
		#check if something is in uploaded/ if so count it
		inUploaded = len(glob.glob('**/uploaded/' + '*.zip', recursive = True)) + 1 #check if something is in uploaded/ and if so store cunter
		if inUploaded < 10:
			numStr = '00' + str(inUploaded)
		elif inUploaded < 100:
			numStr = '0' + str(inUploaded)
		else:
			numStr = str(inUploaded)
		#move file tmp/ -> uploaded/ and add counter
		shutil.move(targetFile, 'uploaded/' + numStr + '_' + targetFile[4:])
		
		#wait(len(glob.glob('**/waiting/' + '*_*.zip', recursive = True)), numInt, config)	
		wait(numInt, config)	

def wait(uploadedFiles, config):
	waitTime = 60 * int(config['server']['waitTime'])
	for i in range(waitTime,0,-1):
		clearConsole()
		print('To next upload: ' + str(i//60) + 'm ' + str(i%60) + 's')
		print('Files uploaded:', str(uploadedFiles))
		print('Files remaining: '+ str(len(glob.glob('**/waiting/' + '*_*.zip', recursive = True))))
		print('Approximate time for remaining files: ' + str((len(glob.glob('**/waiting/' + '*_*.zip', recursive = True)) * waitTime) // 60) + 'm')
		time.sleep(1)

def settings():
	clearConsole()
	print('''
Settings are in Config.ini file

Edit it with notepad, vim or any other text editor of your choice

Enter to continue
	''')
	input()
