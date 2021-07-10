import re
import os
import time
import glob

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def keep_checking(text):
    if(text == ""):
        return False
    else:
        return True


def generate_review(arxivId):

    driver = webdriver.Chrome()
    driver.implicitly_wait(15)

    driver.get("http://review.nlpedia.ai")

    # pdf = glob.glob(f'./modified_pdf/{arxivId}/*.pdf')
    # print(pdf)
    pdf = glob.glob(f'./original_pdf/{arxivId}.pdf')

    if(pdf != []):
        driver.find_element_by_id("file_input").send_keys(os.getcwd() + pdf[0][1:])

        check_box = driver.find_element_by_id("mycb")
        driver.execute_script("arguments[0].click();", check_box)

        upload_btn = driver.find_element_by_id("upload_btn")
        driver.execute_script("arguments[0].click();", upload_btn)
        print("Upload button clicked!")
        time.sleep(10)

        parse_btn = driver.find_element_by_id("parse_btn")
        driver.execute_script("arguments[0].click();", parse_btn)
        print("Parse button clicked!")
        time.sleep(120)

        review_btn = driver.find_element_by_id("review_btn")
        driver.execute_script("arguments[0].click();", review_btn)
        print("Review button clicked!")

        for i in range(120):
            id = driver.find_element_by_id('intro_review')
            if keep_checking(id.text):
                html_list = driver.find_element_by_id('models')
                items = html_list.find_elements_by_tag_name("li")
                main_tab = items[3].find_elements_by_tag_name("a")
                driver.execute_script("arguments[0].click();", main_tab[0])
                absce_review = driver.find_element_by_id('absce_review')
                print("Here is your review: ")
                print("true: ", absce_review.text)
                return absce_review.text
                break
            else:
                time.sleep(5)

        driver.quit()

    else:
        print(f"File Not Found: {arxivId}")


# src_url = '../paper_list.txt'
# dest_url = './reviews/shuffled_reviews.txt'


def Reviews(paper_list, dest_path, no_of_reviews):

    review_file = open(dest_path, "a")

    for i in range(no_of_reviews):
        for j in range(len(paper_list)):
            review = generate_review(paper_list[j])
            if review is None:
                review = ""
                review_file.write(
                    f"{i+1}_" +
                    paper_list[j] +
                    " = " +
                    review +
                    "\n")
            else:
                review_file.write(
                    f"{i+1}_" +
                    paper_list[j] +
                    " = " +
                    review +
                    "\n")
