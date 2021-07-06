import re

path = "../paper_list.txt"


def Get_Id():

    f = open(path)

    paper_list = []

    for x in f:
        grp = re.match(r'(.*)', x)
        paper_list.append(grp.group(1))

    return paper_list
