# Given a folder of files and folders, make all file and folder names lowercase non-recursively

import os
import sys


def main(func_param=None):

    try:
        param = sys.argv[1] if func_param is None else func_param
    except IndexError:
        print("Usage: python rectifier.py <folder>")
        return

    folder = param
    if not os.path.isdir(folder):
        print("Error: folder does not exist")
        return

    print(os.listdir(folder))
    for filename in os.listdir(folder):
        if filename != filename.lower():
            os.rename(os.path.join(folder, filename), os.path.join(folder, filename.lower()))


if __name__ == "__main__":
    main('data')
