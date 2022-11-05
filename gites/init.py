import os
import sys

def git_init():
    os.mkdir(".git/")
    os.mkdir(".git/objects/")
    os.mkdir(".git/refs/")
    with open(".git/HEAD","w") as f:
        f.write("ref: refs/heads/master\n")
        print("created")  
    