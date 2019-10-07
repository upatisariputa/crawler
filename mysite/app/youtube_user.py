from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
import pymysql.cursors
from datetime import datetime

path = "/Users/handanbee/Desktop/chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.youtube.com/channel/UCBvkQFBskQR9NeOoDYR8ckA/about")
page = driver.page_source


try:
    arr = [
        driver.find_element_by_class_name(
            "style-scope ytd-channel-name").text,
        driver.find_element_by_id("subscriber-count").text,
        driver.find_element_by_id("img").get_attribute("src"),
        driver.find_element_by_id("description").text.replace("\n", ''),
        driver.find_element_by_id("right-column").text.replace("\n", ''),
    ]
finally:
    driver.close()

numberToStr = {
    '만명': 10000,
    '천명': 1000
}


subcribeCount = float(arr[1][4:8]) * numberToStr[arr[1][-2:]]
arr[1] = subcribeCount
print(arr[4])
dateN = arr[4][6:19].replace(". ", "-")
# dateN = '2014-12-16'
dateChan = datetime.strptime(dateN, " %Y-%m-%d").date()

print(arr[0], dateChan, arr[3], arr[2], arr[1])

conn = pymysql.connect(host='localhost',
                       user='root',
                       password=None,
                       db='ilio',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_users (user_name, signup_date, user_info, image_url, subscribers_count) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (arr[0], dateChan, arr[3], arr[2], arr[1]))
    conn.commit()
    print(cursor.lastrowid)
    # 1 (last insert id)
finally:
    conn.close()
