from urllib.request import urlopen
import json
import pymysql
import time

URL = "http://bjapi.afreecatv.com/api/kmkm951/vods"
response = urlopen(URL)
page = json.load(response)["meta"]["last_page"]+1

# 현재 년 월 일 주
time = time.localtime()
year = time.tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password=None,
                       db='ilio',
                       charset='utf8mb4')

video_list = []
for i in range(1, page):
    response = urlopen(URL + "?page=" + str(i))
    video_list = json.load(response)
#     print(video_list)
    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_video ( V_name, V_upload, like_A_Y, dislike_Y, view_A_Y_T, comment_A_Y, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for video_info in video_list['data']:
            cursor.execute(sql, (
                video_info["title_name"],
                video_info["reg_date"][0:10],
                video_info["count"]["like_cnt"],
                "0",
                video_info["count"]["read_cnt"],
                video_info["count"]["comment_cnt"],
                year,
                month,
                week,
                day,
                1
            ))

        conn.commit()
        print(cursor.lastrowid)

conn.close()
