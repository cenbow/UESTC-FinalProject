#!python3
# !- coding:utf-8 -
import sys

print(sys.version)

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome('./bin/chromedriver.exe')


def verify(url):
    global driver
    driver.get(url)
    time.sleep(3)
    slider = driver.find_element_by_xpath('//*[@id="nc_1_n1t"]')
    button = driver.find_element_by_xpath('//*[@id="verify"]')
    action = ActionChains(driver)

    action.click_and_hold(slider)
    action.move_by_offset(280, 0).release().perform()
    time.sleep(2)
    action.release()

    action.click(button).perform()


