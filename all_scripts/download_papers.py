import urllib.request
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('./')))
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


def Download_PDF(paper_list, dest_path):

    for i in range(len(paper_list)):
        arxiv_link = 'https://arxiv.org/pdf/' + str(paper_list[i]) + '.pdf'
        urllib.request.urlretrieve(
            arxiv_link,
            f'{dest_path}{paper_list[i]}.pdf',
            show_progress)
