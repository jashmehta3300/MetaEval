import sys, os
import re
import subprocess
import glob
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("./"))
from all_scripts.get_id import Get_Id
from all_scripts.download_latex import download_latex
from all_scripts.scrap_abstracts import get_abstract
from all_scripts.embeddings import Embeddings
from all_scripts.generate_reviews import Reviews
from all_scripts.download_papers import Download_PDF
# from all_scripts.plot_distances import Plot_Distances
from shuffle import shuffle_adj
import json


if __name__ == '__main__':
    paper_list = Get_Id()

    # download_latex(paper_list, './original_src', './original_pdf')
    # download_latex(paper_list, './modified_src', './modified_pdf')

    info = get_abstract(paper_list)
    # with open('./data.json', 'w', encoding='utf-8') as f:
    #     json.dump(info, f, ensure_ascii=False, indent=4)

    # embeddings = Embeddings(info)
    # with open('./embeddings.json', 'w', encoding='utf-8') as f:
    #     json.dump(embeddings, f, ensure_ascii=False, indent=4)

    # Download_PDF(paper_list, "./original_pdf/")

    ids = [i["paper_id"] for i in info]
    abs = [i["abstract"] for i in info]

    no_of_shuffles = 10

    for j in range(no_of_shuffles):

        for i in range(len(ids)):
            file_in_abs = shuffle_adj(ids[i], "./modified_src", abs[i])
            print(file_in_abs)
            files = glob.glob(f"./modified_src/{ids[i]}/*.tex")
            for file in files: 
            # if file_in_abs is not None:
                try:
                    # latex command is used for compilation
                    proc = subprocess.run(["pdflatex",
                                        "-output-directory={}".format(f"./modified_src/{ids[i]}/"),
                                        "-interaction=batchmode",
                                        "-output-format=pdf",
                                        "-silent",
                                        "-shell-escape",
                                        file_in_abs],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=2)
            #         (stdout, stderr) = proc.communicate()
                except subprocess.CalledProcessError as err:
                    continue
            #         print("Error ocurred for latex file {}: ".format(file) + err.stderr)
                except subprocess.TimeoutExpired:
                    continue

                grp = re.match(r'(.*)/(.*).tex', file_in_abs)
                pdf_file = grp.group(2) + ".pdf"
                print(pdf_file)
                cp_pdf = subprocess.run(["cp",
                                        f"./modified_src/{ids[i]}/{pdf_file}",
                                        f"./modified_pdf/{ids[i]}/"])

        Reviews(paper_list, './reviews/reviews.txt', 1)

        download_latex(paper_list, './modified_src', './modified_pdf')

    # Plot_Distances(paper_list, "./reviews/", "./results/")


