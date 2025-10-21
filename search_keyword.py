from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://csrankings.org/")
title = driver.title

region = "us"
publication_fromyear = "2021"
target_univ = "California Institute of Technology"
domain = "robotics"

wait = WebDriverWait(driver, 10) # Wait up to 10 seconds

try:
    element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='all_areas_off']"))
        )
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_selected(driver.find_element("xpath", "//a[@id='all_areas_off']")))
    except:
        pass
    print("Click")

    element.click() # Perform the click action once the element is clickable

    # Select region
    select_element = driver.find_element("xpath", "//select[@id='regions']")
    select = Select(select_element)
    select.select_by_value(region)

    # Select publication from year
    select_element = driver.find_element("xpath", "//select[@id='fromyear']")
    select = Select(select_element)
    select.select_by_value(publication_fromyear)
    
    # Check domain button
    driver.find_element("xpath", f"//input[@id='{domain}']").click()

    # Find professors' google scholar
    wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{target_univ}')]"))
    )
    target_univ_element = driver.find_element("xpath", f"//span[contains(text(),'{target_univ}')]")
    ranking_table_element = driver.find_element("xpath", f"//table[@id='ranking']")
    table_elements = ranking_table_element.find_elements("xpath", "./tbody/tr")
    found_idx = -1
    for id, table_element in enumerate(table_elements):
        # print(id, table_element)
        try:
            span_element = table_element.find_element("xpath", f".//td/span[contains(text(),'{target_univ}')]")
            found_idx = id+1
            print(span_element.text)
        except:
            pass
        if found_idx != -1:
            break
    
    target_univ_element.click()
    # NOTE: Table element is start from 1
    target_univ_table_element = ranking_table_element.find_element("xpath", f"./tbody/tr[{found_idx+2}]")
    
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_selected(driver.find_element("xpath", "//a[@id='all_areas_off']")))
    except:
        pass

    google_scholar_a_elements = target_univ_table_element.find_elements("xpath", ".//a[contains(@href,'scholar.google.com')]")
    for id, google_scholar_a_element in enumerate(google_scholar_a_elements):
        print(id, google_scholar_a_element.get_attribute("href"))
        
    all_univ_scholars_elements = target_univ_table_element.find_elements("xpath", ".//td/small/a[1]")
    all_univ_scholars_elements = all_univ_scholars_elements[::2]
    for scholar_element in all_univ_scholars_elements:    
        print(scholar_element.text)
    
    print(target_univ_table_element.text)
    

    print("Clicked")
    WebDriverWait(driver, 10).until(EC.element_to_be_selected(driver.find_element("xpath", "//a[@id='all_areas_on']")))
except TimeoutError:
    print("Element not clickable within the specified timeout.")
except Exception as e:
    print(e)
element_test = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='inforet']"))
    )
# driver.quit()
