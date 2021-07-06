import sys, os
import re
import subprocess
import glob
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("./"))
from all_scripts.get_id import Get_Id
from all_scripts.generate_reviews import Reviews
from all_scripts.download_papers import Download_PDF
# from all_scripts.plot_distances import Plot_Distances
import json


if __name__ == '__main__':
    paper_list = Get_Id()

    Download_PDF(paper_list, "./original_pdf/")

    Reviews(paper_list, './reviews/reviews.txt', 1)

    # Plot_Distances(paper_list, "./reviews/", "./results/")


