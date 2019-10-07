from selenium import webdriver
import time
import json
from selenium.webdriver.common.keys import Keys
import pymysql.cursors
from datetime import datetime

path = "/Users/handanbee/Desktop/chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.youtube.com/channel/UCu750LH-nGQetXoosDwcWOg/videos")
page = driver.page_source


SCROLL_PAUSE_TIME = 2
# Get scroll height
"""last_height = driver.execute_script("return document.body.scrollHeight")
this dowsnt work due to floating web elements on youtube
"""
last_height = driver.execute_script(
    "return document.documentElement.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script(
        "window.scrollTo(0,document.documentElement.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    if new_height == last_height:
        print("break")
        break
    last_height = new_height
