from typing import List

from os import listdir
from os.path import isfile, join


def file_to_lines(filename, strip_=False) -> List[str]:
    with open(filename) as file:
        lines = file.readlines()
        if strip_:
            lines = [l.strip() for l in lines if l.strip()]
        return lines


def save_to_file(text: str, filepath: str, mode='w'):
    with open(filepath, mode) as file:
        file.write(text)
        print("written file: ", filepath)


def all_filenames_in_directory(directorypath: str) -> List[str]:
    onlyfiles = [f for f in listdir(directorypath) if isfile(join(directorypath, f))]
    return onlyfiles


def filenames_in_directory_containing_substring(directorypath: str, substring: str, fullpath=False) -> List[str]:
    files = [f for f in all_filenames_in_directory(directorypath) if substring in f]
    if(fullpath):
        files = [join(directorypath, f) for f in files]
    return files