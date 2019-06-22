#/usr/bin/python

import os
import system
import shutil
import subprocess

#Quick base directory for reference.
directory1 = "/A2A2J"
directory2 = "/A2A2J/ASANLOGS/"
directory3 = "/A2A2J/DUPL_CRASH_FILES/"

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
Y = YEL + "[!?]" + END

#Let's start building our work directories. Hit enter to just skip this all if they exist. 
buildDirs = raw_input(R + "Create work directories? y/n/enter to skip if they exist.\n")
#Don't want to try to build them.
if buildDirs == "n":
	print (G + "Not building directories. Skipped.\n")
#They exist already.
elif os.path.isdir(directory1) is True and buildDirs == "y":
	print (G + "Directory exists.\n")
#If they do not exist and you want them made.
elif os.path.isdir(directory1) is False and buildDirs == "y":
	
	print(G + "Creating work directories: /A2A2J/, /A2A2J/ASANLOGS/, and /A2A2J/DUPL_CRASH_FILES/")
	#Make them.
	os.mkdir( directory1, 0755 )
	os.mkdir( directory2, 0755 )
	os.mkdir( directory3, 0755 )
	print(G + "Created directories.")
else:
	#Blank input and/or skip.
	print (Y + "Nothing? Skipped.")

#GRAB ASAN BINARY
asanBinary = raw_input(R + "Where is the location for the ASAN-compiled binary? File path like this:\n/exact/path/to/the/binary\n")
if os.path.isfile(asanBinary) is True:
	#Seriously.
	print (G + "Found. Your job to make sure it has ASAN enabled.")
	#Where is it?
elif path.isfile(asanBinary) is False:
	print (Y + "Doesn't seem to exist?")
	exit(1)
else:
	print (Y + "Nothing? Skipped.")

#GRAB OUR ORIGINAL CRASH FILES LOCATION
crashLocation = raw_input(R + "Where is the location for the AFL out/ folder? File path like this:\n/exact/path/to/folder/out/\n")

if path.isdir(crashLocation) is True:
	print (G + "Found. Your job to make sure it has crash files.\n")
	#COPY ORIGINAL CRASH FILES TO WORK DIRECTORY
	copyFiles = raw_input(R + "Copy crash files to working directory? y/n/enter to skip\n")
	if copyFiles == "y":
		for directoryname in os.listdir(crashLocation):
			crashFolders = crashLocation + directoryname + "/crashes/"
			for filename in os.listdir(crashFolders):
				crashFiles = crashFolders + filename
				#Copy all of the files found in all of the crashes folders found.
				print(Y + "This can take a few minutes to complete copying.\n")
    			shutil.copy( crashFiles, directory3)
    			print (G + "Done!")
    elif copyFiles == "n":
    	print (Y + "Skipped.")
    else:
    	print (Y + "Nothing? Skipped.")

elif path.isdir(crashLocation) is False:
	print (Y + "Doesn't seem to exist?")
	exit(1)
else:
	print (Y + "Nothing? Skipped.")


generateASANLOG = raw_input(R + "Generate ASANLOGS from ASAN Binary? y/n\n")
if generateASANLOG == "y":
	print(G + "Let's burn some CPU cycles up. Building an ASANLOG in /A2A2J/ASANLOG/")
	bashCommand = "bash -c 'for i in $(ls " + str(directory3) + "); do " + str(asanBinary) + " $i; done &>" + str(directory2) + "/ASANLOG.txt ; echo \"FINISHED_FINISHED_FINISHED\" >> " + str(directory2) + "ASANLOG.txt'"
	subprocess.run(bashCommand,
    shell=True, check=True,
    executable='/bin/bash')

else:
	print (Y + "Nothing? Skipped.")
