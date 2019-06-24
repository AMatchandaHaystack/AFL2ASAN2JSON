# AFL2ASAN2JSON
A small helpful program to quickly cover AFL-fuzz generated crash files against an AddressSanitizer / ASAN-instrumented binary and convert those log components to a JSON payload for parsing. Code is heavily commented to follow the simple workflow of the script: Input -> copy crashes -> generate script -> generate ASAN logs -> convert to JSON.
