import threading
from os import system
from sys import argv
from requests import get
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
                get(url)
            else:
                system("curl " + url + " &> /dev/null")
            if verbose:
                ping_count += 1
                print("Thread pinged: " + url + " Total: " + str(ping_count) + " ID: " + str(num))

try:
    url = argv[1]
except IndexError:
    print("No URL provided", file=sys.stderr)
    exit(1)

try:
    thread_count = int(argv[2]) + 1
except IndexError:
    print("No thread count provided", file=sys.stderr)
    exit(1)

ping_count = 0
verbose = False
py = False

if "-v" in argv:
    verbose = True

if "-p" in argv:
    py = True

generate(url, thread_count, verbose, py)
