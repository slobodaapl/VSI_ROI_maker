# Given a folder of files and folders of the format
# folder: _<number>_<he|p63>_
# file: <number>_<he|p63>.vsi
# this script will validate that the files and folders are in the correct format and that for each folder there is a corresponding file

import os
import re


def validate_folder(folder):
    # check that the folder name is in the correct format
    # folder: _<number>_<he|p63>_
    if not re.match(r'^_\d+_(he|p63)_$', folder):
        print("Invalid folder name: " + folder)
        return False
    return True


def validate_file(file):
    # check that the file name is in the correct format
    # file: <number>_<he|p63>.vsi
    if not re.match(r'^\d+_(he|p63).vsi$', file):
        print("Invalid file name: " + file)
        return False
    return True


def check_all(directory: str):
    # get a list of all files excluding folders
    files = [f for f in os.listdir(directory) if os.path.isfile(f)]
    # get a list of all folders
    folders = [f for f in os.listdir(directory) if os.path.isdir(f)]

    # check that all files and folders are correct format
    for file in files:
        if not validate_file(file):
            return False
    for folder in folders:
        if not validate_folder(folder):
            return False

    # check that for each folder there is a corresponding file
    for folder in folders:
        # get the number from the folder name
        number = re.search(r'\d+', folder).group(0)
        # check that the corresponding file exists
        if not any(number in file for file in files):
            print("No corresponding file for folder: " + folder)
            return False
    return True


if __name__ == "__main__":
    check_all('data')
