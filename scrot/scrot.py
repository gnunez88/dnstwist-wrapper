#!/usr/bin/python3

import argparse
import logging
import pathlib
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from colorama import Fore, Back, Style
#from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt

# Global variables
dependencies = [
    'wkhtmltoimage'
]
#RESET = Fore.NORMAL + Back.NORMAL + Style.NORMAL

# Functions
def stop(sig, frame):
    sys.stderr.write('\n[!] Exiting...\n')
    sys.exit(1)


def check_dependencies() -> bool:
    global dependencies
    success = True
    for dependency in dependencies:
        path = shutil.which(dependency)
        if path:
            print(f"{Fore.GREEN + Style.BRIGHT}{dependency}{Style.RESET_ALL} found.")
        else:
            print(f"{Fore.RED + Style.BRIGHT}{dependency}{Style.RESET_ALL} not found.")
            success = False
    return success


def capture_screenshot(url:str, outfile:str) -> bool:
    command = f"wkhtmltoimage -f png {url} {outfile}"
    process = subprocess.run(command.split(), capture_output=True)
    return True if process.returncode == 0 else False


# Standalone
def main(args):
    signal.signal(signal.SIGINT, stop)
    init_time = time.perf_counter()
    if args.verbose > 0:
        print(f"Initial time: {init_time}")

    if not check_dependencies():
        error_message = "There are some dependencies missing."
        sys.stderr.write(f"\n{error_message}\n")
        sys.exit(2)

    if args.file:
        with open(args.target, 'r') as f:
            urls = f.read().split('\n')
            # Removing empty lines
            urls = list(filter(lambda x: not re.match(r'^\s*$', x), urls))
    else:
        urls = [args.target]

    #with ThreadPoolExecutor(max_workers=10) as executor:
    #    executor.map(...)
    date = dt.now().strftime("%Y-%m-%d")

    path_dir = pathlib.Path(f"{args.outdir}/{date}")
    if not path_dir.exists():
        path_dir.mkdir(parents=True, exist_ok=True)

    threads = list()
    for url in urls:
        domain_pattern = r'[\w-]+\.\w{2,5}(?:(:\d|/|$))'
        domain = re.search(domain_pattern, url).group()  # This can raise an exception
        timestamp = dt.now().strftime("%H%M%S")
        path_file = f"{path_dir}/{domain}_{timestamp}.png"
        t = threading.Thread(target=capture_screenshot, args=[url, path_file])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()
    if args.verbose > 0:
        print(f"Ending time: {end_time}")
        print(f"Elapsed time: {end_time - init_time}")


if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str, help="Target URL")
    parser.add_argument('-o', '--outfile', type=str, help="Output file to save the capture")
    parser.add_argument(
            '-d', '--outdir', 
            type=str, 
            default="results/img",
            help="Path to output directory. Default: %(default)s")
    parser.add_argument('-f', '--file', action='store_true', help="The input is a file")
    parser.add_argument('-v', '--verbose', action='count', default=0, help="Verbose mode")
    parser.add_argument(
            '-l', '--loglevel', 
            type=str, 
            default="info", 
            choices=["debug", "info", "warn", "error", "crit"],
            help="Logging level. Default: %(default)s")
    args = parser.parse_args()
    # Logging
    loglevels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "error": logging.ERROR,
            "crit": logging.CRITICAL
        }
    fmt = "[%(asctime)s] %(message)s"
    dfmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
            format=fmt, 
            level=loglevels[args.loglevel], 
            datefmt=dfmt,
            filename=f'scrot_{dt.now().strftime("%Y-%m-%d-%H%M%S")}.log')
    # Calling main function
    main(args)
