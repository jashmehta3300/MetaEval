import glob
import subprocess
import re
from get_id import Get_Id

# paper_list_path = "../paper_list.txt"
# src_files = "./papers_src"


def Compile_Latex_All(paper_list_path, src_files):

    for arxivId in list(set(Get_Id(paper_list_path))):

        # read all latex files
        files = glob.glob(f"{src_files}/{arxivId}/*.tex")

        # path to store compiled pdf files
        # (gives error if dest is in different folder)
        dest_path = f"{src_files}/{arxivId}/"

        # compile files into pdf
        for file in files:
            try:
                # latex command is used for compilation
                proc = subprocess.run(["pdflatex",
                                       "-output-directory={}".format(dest_path),
                                       "-interaction=batchmode",
                                       "-output-format=pdf",
                                       "-silent",
                                       "-shell-escape",
                                       file],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      timeout=2)
        #         (stdout, stderr) = proc.communicate()
            except subprocess.CalledProcessError as err:
                continue
        #         print("Error ocurred for latex file {}: ".format(file))
                # print(err.stderr)
            except subprocess.TimeoutExpired:
                continue
