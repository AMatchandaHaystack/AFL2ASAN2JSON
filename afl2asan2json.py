#!/usr/bin/python3

import os
import time
import shutil
import base64
import subprocess

#Quick base directory for reference.
directory1 = "/A2A2J"
directory2 = "/A2A2J/ASANLOGS/"
directory3 = "/A2A2J/DUPL_CRASH_FILES/"
directory4 = "/A2A2J/COMMAND_LOGS/"

#Nifty terminal trick for display colors.
#RED
RED = '\033[91m'
END = '\033[0m'
R = RED + "[?]" + END

#GREEN
GRE = '\033[92m'
G = GRE + "[o]" + END

#YELLOW
YEL = '\033[93m'
Y = YEL + "[!]" + END

#BLUE
BLU = '\033[94m'



#Let's start building our work directories. Hit enter to just skip this all if they exist.
buildDirs = raw_input(R + "Create work directories? y/n/anything else to skip ")
#Don't want to try to build them.
if buildDirs == "n":
	print (G + "Not building directories. Skipped.\n")
#They exist already.
elif os.path.isdir(directory1) is True and buildDirs == "y":
	print (G + "Directory exists.\n")
#If they do not exist and you want them made.
elif os.path.isdir(directory1) is False and buildDirs == "y":
	print(G + "Creating work directory: /A2A2J/")
	print(G + "Creating work directory: /A2A2J/ASANLOGS/")
	print(G + "Creating work directory: /A2A2J/COMMAND_LOGS/")
	print(G + "Creating work directory: /A2A2J/DUPL_CRASH_FILES/")
#Make them.
	os.mkdir(directory1, 0755)
	os.mkdir(directory2, 0755)
	os.mkdir(directory3, 0755)
	os.mkdir(directory4, 0755)
	print(G + "Created directories.\n")
else:
#Blank input and/or skip.
	print (Y + "Nothing? Skipped.")

#GRAB ASAN BINARY
asanBinary = raw_input(R + "Where is the location for the ASAN-compiled binary? File path like this:\n/exact/path/to/the/binary\n")
if os.path.isfile(asanBinary) is True:
#Seriously.
	print (G + "Found. Your job to make sure it has ASAN enabled.\n")
	commandOps = raw_input(R + "Did you need to run it with any command line switches? y/n ")
	if commandOps == "y":
		switchOps = raw_input(Y + "Input command line switches.\n" + Y + "An initial space for formatting is included.\n" + Y +"Provide input like this all in one line: -r --options X etc.\n")
		print (G + "Stored: " + asanBinary + " " + switchOps)
	else:
		print (G + "No options used.\n")
		switchOps = ""
#Where is it?
elif os.path.isfile(asanBinary) is False:
	print (Y + "Doesn't seem to exist?")
	exit(1)
else:
	print (Y + "Nothing? Skipped.")

#GRAB OUR ORIGINAL CRASH FILES LOCATION
crashLocation = raw_input(R + "Where is the location for the AFL out/ folder? File path like this:\n/exact/path/to/folder/out/\n")

if os.path.isdir(crashLocation) is True:
	print (G + "Found. Your job to make sure it has crash files.\n")
#COPY ORIGINAL CRASH FILES TO WORK DIRECTORY
	copyFiles = raw_input(R + "Copy crash files to working directory? y/n/anything else to skip ")
	if copyFiles == "y":
		for directoryname in os.listdir(crashLocation):
			crashFolders = crashLocation + directoryname + "/crashes/"
			for filename in os.listdir(crashFolders):
				crashFiles = crashFolders + filename
#Copy all of the files found in all of the crashes folders found.
				print(Y + "This can take a few minutes to finish copying.")
				shutil.copy(crashFiles, directory3)
				print (G + "Done!\n")
	else:
		print (Y + "Skipped.")
elif os.path.isdir(crashLocation) is False:
	print (Y + "Doesn't seem to exist?")
	exit(1)
else:
	print (Y + "Nothing? Skipped.")

#Run a bash for loop with our ASAN-compiled binary against all of the crash files.
generateASANLOG = raw_input(R + "Generate ASANLOGS from ASAN Binary? y/n ")
if generateASANLOG == "y":
#Build script to generate ASAN logs.
	if switchOps == "":
		bashCommand = "for i in " + str(directory3) + "*; do " + str(asanBinary) + " $i; done"
	else:
		bashCommand = "for i in " + str(directory3) + "*; do " + str(asanBinary) + " " + switchOps + " $i; done"
	print (Y + "Built your script as: " + BLU + str(bashCommand) + str(switchOps) + END + ".")
	print (Y + "Please review carefully.")
	print (Y + "You may need to modify the bash command in a2a2j source (bashCommand variable) to match your particular binary.\n")
	commandGood = raw_input(R + "Does this command appear correct? Only 'y' to continue. ")
	if commandGood != "y":
		print(Y + "Sorry about that, may need to edit the source of this script.")
		exit(1)
	else:
		print(G + "Proceeding.")
#Generate a unique timestamp.
	timeStamp = time.strftime("%b%d%Y%H:%M:%S", time.localtime())
#Name our scriptlog after the base64encoded name of the timestamp so it is easily recovered while still unique.
	fileName = base64.b64encode(timeStamp)
#Color format blue for important locations.
	B1 = BLU + directory4 + fileName + ".sh" + END
#Create scriptlog and write command to it for execution.
	writeScript = open(r"/A2A2J/COMMAND_LOGS/" + fileName + ".sh","w+") 
	writeScript.write(str(bashCommand))
	writeScript.close()
	print (G + "Built script " + B1 + " to generate ASAN logs.")
#Color format blue for important locations again.
	logLocation = directory2 + "ASANLOG.txt"
	B2 = BLU + logLocation + END
	print (G + "Now executing and writing log to " + B2)
#Execute scriptlog.
	executeScript = "/bin/bash " + str(directory4) + str(fileName) + ".sh"
	print(G + "Generating!")
	os.system(executeScript + " 1> /dev/null 2>" + str(directory2) + "/ASANLOG.txt ; echo \"FINISHED_FINISHED_FINISHED\" >> " + str(directory2) + "ASANLOG.txt")
	print(G + "Done!")
else:
	print (Y + "Skipped.")
