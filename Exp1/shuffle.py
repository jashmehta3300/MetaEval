import glob
import subprocess
import re
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# src_path = "./modified_src"


def shuffle_abs(arxivId, src_path, abs):

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
            print(list_abs)
            random.shuffle(list_abs)
            final_abs = '.'.join(list_abs)
            print(final_abs)
            texdoc.insert(start + 1, final_abs)

            with open(file, 'w') as fin:
                for i in range(len(texdoc)):
                    fin.write(texdoc[i])

            return file


def shuffle_abs_asc(arxivId, src_path, abs):
    
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
            print(list_abs)
            len_dict = {}
            for i in range(len(list_abs)):
                len_dict[len(list_abs[i])] = list_abs[i]
            print("len_dict: ",len_dict)
            marklist = sorted(len_dict.items(), key=lambda x:x[0])
            sortdict = dict(marklist)
            print("sorted: ", sortdict)
            shuffled = sortdict.values()
            final_abs = '. '.join(shuffled)
            print("final_abs: ", final_abs)
            texdoc.insert(start+1, final_abs)

            with open(file, 'w') as fin:
                for i in range(len(texdoc)):
                    fin.write(texdoc[i])

            return file

def shuffle_abs_dec(arxivId, src_path, abs):
    
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
            print(list_abs)
            len_dict = {}
            for i in range(len(list_abs)):
                len_dict[len(list_abs[i])] = list_abs[i]
            print("len_dict: ",len_dict)
            marklist = sorted(len_dict.items(), key=lambda x:x[0], reverse=True)
            sortdict = dict(marklist)
            print("sorted: ", sortdict)
            shuffled = sortdict.values()
            final_abs = '. '.join(shuffled)
            print("final_abs: ", final_abs)
            texdoc.insert(start+1, final_abs)

            with open(file, 'w') as fin:
                for i in range(len(texdoc)):
                    fin.write(texdoc[i])

            return file

