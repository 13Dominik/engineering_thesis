import os
import random
import subprocess
import sys
import time
from typing import List

def load_links() -> List[str]:
    with open("links2.csv", mode='r') as file:
        return [line.strip() for line in file.readlines()]


script_name = "allegro.py"

args = load_links()

i = 0
arg = args[i]

while True:
    try:
        result = subprocess.run([sys.executable, script_name] + [arg], check=True, capture_output=True, text=True)
        # Check output
        if result.returncode == 0:
            # if everything was correct go to another product
            i += 1
            # check if link is last on the list
            if i == len(args):
                break
            arg = args[i]
            time.sleep(random.randint(15, 25))
    except subprocess.CalledProcessError as e:
        # If reviews of this product in database, go to the next link
        if "ProductInDatabase" in e.stderr:
            i += 1
            if i == len(args):
                break
            arg = args[i]
            time.sleep(random.randint(15, 25))
        # If the error is on Allegro site (occures sometimes)
        else:
            time.sleep(random.randint(15, 25))
            continue
