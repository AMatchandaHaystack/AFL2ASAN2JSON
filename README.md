# AFL2ASAN2JSON
A small helpful program to quickly cover AFL-fuzz generated crash files against an AddressSanitizer / ASAN-instrumented binary and convert those log components to a JSON payload for parsing. Code is heavily commented to follow the simple workflow of the script: Input -> copy crashes -> generate script -> generate ASAN logs -> convert to JSON.

root@fuzzbox:/home/Desktop# python afl2asan2json.py 
[!]Requires jq tool.
[?]Create work directories? y/n/anything else to skip y
[o]Creating work directory: /A2A2J/
[o]Creating work directory: /A2A2J/ASANLOGS/
[o]Creating work directory: /A2A2J/COMMAND_LOGS/
[o]Creating work directory: /A2A2J/DUPL_CRASH_FILES/
[o]Creating work directory: /A2A2J/JSON_BLOCK_FILES/
[o]Created directories.

[?]Where is the location for the ASAN-compiled binary? File path like this:
/exact/path/to/the/binary
/home/Desktop/Fuzzers/targets/somebinary
[o]Found. Your job to make sure it has ASAN enabled.

[?]Did you need to run it with any command line switches? y/n y
[!]Input command line switches.
[!]An initial space for formatting is included.
[!]Provide input like this all in one line: -r --options X etc.
--youroptions
[o]Stored: /home/Desktop/Fuzzers/targets/somebinary --youroptions
[?]Where is the location for the AFL out/ folder? File path like this:
/exact/path/to/folder/out/
/media/somefolder/OtherData/out/
[o]Found. Your job to make sure it has crash files.

[?]Copy crash files to working directory? y/n/anything else to skip y
[!]This can take a few minutes to finish copying.
[o]Done!

[?]Generate ASANLOGS from ASAN Binary? y/n y
[!]Built your script as: for i in /A2A2J/DUPL_CRASH_FILES/*; do /home/Desktop/Fuzzers/targets/somebinary $i && echo FILE:$i >>/A2A2J/ASANLOGS/ASANLOG.txt; done.
[!]Please review carefully.
[!]You may need to modify the bash command in a2a2j source (bashCommand variable) to match your particular binary.

[?]Does this command appear correct? Only 'y' to continue. y
[o]Proceeding.
[o]Built script /A2A2J/COMMAND_LOGS/SnVuMjMyMDE5MjM6MDc6MTE=.sh to generate ASAN logs.
[o]Now executing and writing log to /A2A2J/ASANLOGS/ASANLOG.txt
[o]Generating!
[!]This can take several minutes depending on the binary's speed, the number of crash files, and other factors.
[o]Done!

[!]Running quick sanity check on our logs.
[o]Found AddressSanitizer strings in /A2A2J/ASANLOGS/ASANLOG.txt. Log appears sane.

[?]Parse logs to JSON payloads in /A2A2J/JSON_BLOCK_FILES/ ? y/n y
[o]Parsing /A2A2J/ASANLOGS/ASANLOG.txt...
[o]Built block files. Converting to JSON to be parsed by endpoint.
[!]This can take a minute because of the number of files and cleanup. Please wait.
[o]Individual JSON block files based on ASAN logs from AFL's crash files are now ready to be sent upstream to your API!
root@fuzzbox:/home/Desktop# cat /A2A2J/JSON_BLOCK_FILES/
Display all 2936 possibilities? (y or n)

