from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

import os
import json
import pickle

# options = Options()
# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
# options.add_argument(f'--user-agent={user_agent}')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.get("https://scholar.google.com/")
if os.path.exists("cookies.pkl"):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print(cookies)
driver.get("https://scholar.google.com/citations?user=TjWwqmwAAAAJ&hl=en&oi=ao$sortby=pubdate")
    
title = driver.title

region = "us"
publication_fromyear = "2021"
target_univ = "California Institute of Technology"
domain = "robotics"

wait = WebDriverWait(driver, 30) # Wait up to 10 seconds

try:
    element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Year')]"))
        )
    element.click() # Perform the click action once the element is clickable
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    while True:
        try:
            # driver.find_element("xpath", "//span[contains(text(),'Show more')]")
            show_more_element = driver.find_element("xpath", "//button[span/span[contains(text(),'Show more')]]")
            if show_more_element.get_attribute("disabled"):
                break
            # print(EC.element_to_be_clickable((By.XPATH, "//button[span/span[contains(text(),'Show more')]]"))(driver))
        except:
            break
        element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[span/span[contains(text(),'Show more')]]"))
            )
        element.click() # Perform the click action once the element is clickable
    
        import time
        time.sleep(1)
    
    # WebDriverWait(driver, 10).until(EC.element_to_be_selected(driver.find_element("xpath", "//a[@id='all_areas_on']")))
except TimeoutError:
    print("Element not clickable within the specified timeout.")
except Exception as e:
    print(e)
    
publication_table_element = driver.find_element("xpath", "//table[@id='gsc_a_t']")
table_elements = publication_table_element.find_elements("xpath", "./tbody/tr")
publication_lst = []
filter_pubyear = 2021
for id, table_element in enumerate(table_elements):
    pubyear = int("0"+table_element.find_element("xpath", "./td[3]").text)
    pubname = table_element.find_element("xpath", "./td[1]/a").text
    if pubyear >= filter_pubyear:
        publication_lst.append(pubname.lower())
        
filter_keywords = ["phys", "prior", "motion"]
# print(publication_lst)
filtered_publication = []
for publication in publication_lst:
    for filter_keyword in filter_keywords:
        if filter_keyword in publication:
            filtered_publication.append(publication)
            break
print(filtered_publication)
# element_test = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//input[@id='inforet']"))
#     )
driver.quit()
