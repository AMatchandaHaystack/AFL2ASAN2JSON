#include <sys/stat.h> 
#include <sys/types.h> 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


/*program flow =
Step 1) Make working directories
Step 2) Ask for out/ folder for AFL instance crashes
Step 3) Ask for exact location of ASAN-instrumented binary
Step 4) Duplicate crash files. Run a bash loop to bypass to input limit of the "cp" tool. 
Step 5) Generate ASAN logs. Run a bash loop with the binary against duplicated files via STDERR to a working directory.
Step 6) Parse ASAN logs.
Step 7) Build a JSON payload to send to API endpoint. 
*/

char createDirectories(){

	//make init directories
	printf("%s", "[X]Creating directories: \n[o]A2A2J/\n[o]A2A2J/ASANLOGS/\n[o]A2A2J/DUPL_CRASH_FILES/\n\n");
	mkdir("/A2A2J", 0755);
	mkdir("/A2A2J/ASANLOGS/", 0755);
	mkdir("/A2A2J/DUPL_CRASH_FILES/",0755); 
	return 0;
	
}

char main(){
	createDirectories();

	//request out/ folder for AFL instances
	printf("%s", "[X]Where is our out/ folder from AFL?\n[o]Expected input: /path/to/AFL/out/\n[o]Maximum 301 character limit:\n\n"); //try to avoid BOF
	char aflcrashesLocation[305] = "0"; //hope your hostname is short
	fgets(aflcrashesLocation, sizeof(aflcrashesLocation), stdin); //write your input to string


	//request ASAN instrumented binary for generating logs
	printf("%s", "\n[X]What is our ASAN Binary to generate our ASAN logs? [o]Input expected: /here/is/the/binary.somefile\n[o]Maximum 301 character limit:\n\n");
	char asanbinarylocation[305] = "0";
	fgets(asanbinarylocation, sizeof(asanbinarylocation), stdin);


	//first bash loop to copy crash files to duplicate folder
	char commandString[500];
	char summonBash[30] = "bash -c 'for i in $(ls ";
	char endLoop[60] = "); do cp $i/crashes/* /A2A2J/DUPL_CRASH_FILES/; done'"; //CP DOESN'T DO WELL WITH LONG ARGS LISTS SO WE COPY EACH AT A TIME ITERATING OVER THE DIRECTORY.
	
	strcat (commandString, summonBash);
	strcat (commandString, aflcrashesLocation); 
	strcat (commandString, endLoop); 

	system(commandString);	//FILES SHOULD BE COPIED OVER
	
	//second bash loop to make logs by running binary against crash dups
	char runBin[500];
    char summonBashAgain[80] = "bash -c 'for i in $(ls /A2A2J/DUPL_CRASH_FILES/); do ";
    char asanLog[50] = " &> /A2A2J/ASANLOGS/ASANLOG.txt"; 

	strcat(runBin, summonBashAgain);
	strcat(runBin, asanbinarylocation); //such a copout from a loop I know. Don't know if you can force STDERR to a file in C nicely.
	strcat(runBin, asanLog);

	system(runBin); //create logs

}
