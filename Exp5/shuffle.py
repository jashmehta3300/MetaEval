import glob
import subprocess
import re
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from random import randrange

# src_path = "./modified_src"


def shuffle(arxivId, src_path, abs):

    # read all latex files
    files = glob.glob(f"{src_path}/{arxivId}/*.tex")
    print("Searching files: ", files)

    for file in files:
        print("Hi")
        texdoc = []

        f = open(file)
        with open(file) as fin:
            for line in fin:
                texdoc.append(line)

        text_start = "\begin{abstract}"
        text_end = "\end{abstract}"

        text_start_val = [fuzz.ratio(text_start, i) for i in texdoc]
        text_end_val = [fuzz.ratio(text_end, i) for i in texdoc]

        if (max(text_start_val) > 79) and (max(text_end_val) > 79):

            print()
            print(
                f"Text Start match found in: {file} at line number: {text_start_val.index(max(text_start_val))+1} with score: {max(text_start_val)}")
            print(
                f"Text End match found in: {file} at line number: {text_end_val.index(max(text_end_val))+1} with score: {max(text_end_val)}")
            print()

            start = text_start_val.index(max(text_start_val))
            end = text_end_val.index(max(text_end_val))

            for i in range(start + 1, end):
                texdoc[i] = ""

            list_abs = abs.split(".")
            print("Original: ", list_abs)

            max_range = len(list_abs)
            p = randrange(max_range)
            list_abs = list_abs[p:] + list_abs[:p]
            print(p, "Rotated: ", list_abs)

            final_abs = '. '.join(list_abs)
            texdoc.insert(start+1, final_abs)

            with open(file, 'w') as fin:
                for i in range(len(texdoc)):
                    fin.write(texdoc[i])

            return file
