import os
import time

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_abstract(arxivIds):

    titles = []
    abstracts = []

    driver = webdriver.Chrome()
    driver.implicitly_wait(15)

    for i in range(len(arxivIds)):

        driver.execute_script("window.open('');")

        id = arxivIds[i]
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://arxiv.org/abs/{id}")

        title_ele = driver.find_elements_by_xpath('//h1[@class="title mathjax"]')[0]
        titles.append(title_ele.text)

        abs_ele = driver.find_element_by_tag_name("blockquote")
        abstracts.append(abs_ele.text)
        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

    info = []
    for i in range(len(arxivIds)):
        info.append({"paper_id": arxivIds[i],
                     "title": titles[i],
                     "abstract": abstracts[i]})

    return info
