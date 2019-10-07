from myapi.models import Platform
from selenium import webdriver
from urllib.request import Request, urlopen
import json
import pymysql
import time
import django
import os
import sys

sys.path.append("mysite/myapi/models.py")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


if __name__ == "__main__":
    print(Platform.objects.all())

# 크롬 headless 설정(크롬 창이 뜨지 않게 된다.)
options = webdriver.ChromeOptions()
options.add_argument('headless')

# # 팬클럽, 서포터  수 정보
# URL = "http://bjapi.afreecatv.com/api/wjddk26/station/detail"
# response = urlopen(URL)
# fanclub = json.load(response)["count"]
# print(fanclub)

# # BJ 정보 , 이름, 썸네일, 구독 ,애청자
# URL = "http://bjapi.afreecatv.com/api/wjddk26/station"
# req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
# response = urlopen(req)
# bj_info = json.load(response)
# # 현제 년,월,일,주
# time = time.localtime()
# year = time.tm_year
# month = time.tm_mon
# day = time.tm_mday
# week = int(time.tm_yday/7)
# createtime = str(year)+str(month)+str(day)

# img = bj_info["profile_image"]
# introduce = bj_info["station"]["display"]["profile_text"]
# name = bj_info["station"]["user_nick"]
# fav_fan = bj_info["station"]["upd"]["fan_cnt"]
# signup = bj_info["station"]["jointime"]

# print(img, "\n", introduce, "\n", name, "\n", "\n", fav_fan, "\n", signup)

# conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password=None,
#                        db='ilio',
#                        charset='utf8mb4')

# with conn.cursor() as cursor:
#     sql = 'INSERT INTO myapi_subscribe (created_at, S_count, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
#     cursor.execute(sql, (createtime, fav_fan, year, month, week, day, "2"))
#     conn.commit()
#     print(cursor.lastrowid)
# try:
#     with conn.cursor() as cursor:
#         sql = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
#         cursor.execute(sql, (name, img, introduce, signup, "2"))
#         conn.commit()
#         print(cursor.lastrowid)
# finally:
#     conn.close()


# Today = Subsribe.objects.filter(P_userkey=userkey).filter(
#     Y=year).filter(M=month).filter(D=day)
# yesterday = Subsribe.objects.filter(P_userkey=userkey).filter(
#     Y=tear).filter(M=month).filter(D=day-1)

# TWsub = Subsribe.objects.filter(
#     P_userkey=userkey).filter(Y=year).filter(W=week)
# LWsub = Subsribe.objects.filter(
#     P_userkey=userkey).filter(Y=year).filter(W=week-1)

# TMsub = Subsribe.objects.filter(
#     P_userkey=userkey).filter(Y=year).filter(M=month)
# LMsub = Subsribe.objects.filter(
#     P_userkey=userkey).filter(Y=year).filter(M=month-1)
