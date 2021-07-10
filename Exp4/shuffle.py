import glob
import subprocess
import re
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import random
import spacy
nlp = spacy.load("en_core_web_sm")
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet


def find_opposite(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    antonyms = list(set(antonyms))
    random.shuffle(antonyms)
    if len(antonyms) == 0:
        return word
    else:
        return antonyms[0]

def shuffle_adj(arxivId, src_path, abs):

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

            doc = nlp(abs)
            final_text = ''
            for tok in doc:
                if tok.pos_ == 'ADJ':
                    tok = find_opposite(str(tok))
                final_text += str(tok) + ' '
            print(final_text)
            texdoc.insert(start+1, final_text)

            with open(file, 'w') as fin:
                for i in range(len(texdoc)):
                    fin.write(texdoc[i])

            return file
