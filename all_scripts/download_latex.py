import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('./')))

import re
import time
import subprocess
import urllib.request
import progressbar

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

# paper_list_path = "..paper_list.txt"
# dest_path_src = "./papers_src"
# dest_path_comp = "./papers_compiled"


def download_latex(to_download, dest_path_src, dest_path_comp):

    print(to_download)
    base_url = "http://export.arxiv.org/e-print/"

    for iterid, arxivId in enumerate(to_download):

        if (iterid + 1) % 4 == 0:
            time.sleep(2)
        iterid += 1

        try:
            paper_url = base_url + arxivId
            dest_file = f"{dest_path_src}/{arxivId}"

            if arxivId.find("/") > -1:
                clean_id = arxivId.replace("/", "_")
                dest_file = "./papers_src/" + clean_id

            subprocess.run(["mkdir", "-p", f"{dest_path_src}"])
            subprocess.run(["mkdir", "-p", f"{dest_path_comp}"])

            urllib.request.urlretrieve(
                paper_url,
                f'{dest_path_src}/{arxivId}-src',
                show_progress)
            
            subprocess.run(["mkdir", f"{dest_path_src}/{arxivId}"])
            subprocess.run(
                ["mkdir", f"{dest_path_comp}/{arxivId}"])
            subprocess.run(
                ["tar", "-C", dest_file, "-xvf", dest_file + "-src"])
            subprocess.run(["rm", f"{dest_path_src}/{arxivId}-src"])
            print("Done: ", iterid)

        except Exception as ex:
            print(arxivId, ex.__dict__)
            if "code" in ex.__dict__ and ex.code == 403:
                print(ex.msg)
                time.sleep(3)


# download_latex('./papers_src', './papers_compiled')
