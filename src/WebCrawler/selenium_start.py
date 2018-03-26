from selenium import webdriver
from selenium.webdriver import ActionChains
import time

# webdriver.ChromeOptions.binary_location = './bin/chromedriver.exe'

driver = webdriver.Chrome('./bin/chromedriver.exe')
try:
    driver.get('https://www.google.com')

    time.sleep(10)

    search = driver.find_element_by_id('lst-ib')
    # su = driver.find_element_by_id('su')

    action = ActionChains(driver)
    action.send_keys_to_element(search, 'hello world\n').perform()
    time.sleep(5)

finally:
    driver.close()

