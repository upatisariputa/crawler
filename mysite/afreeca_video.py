import os, json, pymysql, time
from urllib.request import Request, urlopen
from django.db.models import Sum

#순서 바꾸면 안된다. 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()
from myapi.models import Platform, Video

# 현재 년 월 일 주
time = time.localtime()
year = time.tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

## Platform table 에서 값을 가져온다. 
p_key = []
p_key = Platform.objects.filter(P_name='afreeca').values('P_key','P_userkey','P_url','P_name')

for i in p_key:
    name = i['P_url'].replace("http://bj.afreecatv.com/", "")
    conn = pymysql.connect(host='localhost',
                          user='root',
                          password=None,
                          db='ilio',
                          charset='utf8mb4')
    URL = "http://bjapi.afreecatv.com/api/"+name+"/vods"
    response = urlopen(URL)
    page = json.load(response)["meta"]["last_page"]+1

    key = i['P_key']
    video_list = []
    for i in range(1, page):
      response = urlopen(URL + "?page=" + str(i))
      video_list = json.load(response)
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
                    key
                ))

            conn.commit()
            # print(cursor.lastrowid)


      T_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(month=month).filter(day=day).values("like_A_Y", "view_A_Y_T","comment_A_Y")
      Y_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(month=month).filter(day=day-1).values("like_A_Y", "view_A_Y_T","comment_A_Y")

      if bool(Y_video):
        for T,Y in zip(T_video, Y_video):
          like = T["like_A_Y"] - Y["like_A_Y"]
          view = T["view_A_Y_T"] - Y["view_A_Y_T"]
          comment = T["comment_A_Y"] - Y["comment_A_Y"]



          with conn.cursor() as cursor:
            sql = "INSERT INTO myapi_d_video_gap (like_A_Y, view_A_Y_T, comment_A_Y, P_key_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (like, view, comment, key))
            conn.commit()
            print(cursor.lastrowid)

      TW_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(week=week).values("like_A_Y", "view_A_Y_T","comment_A_Y")
      LW_video = TW_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(week=week-1).values("like_A_Y", "view_A_Y_T","comment_A_Y")

      W_total = {'like':0 , 'view':0, 'comment':0}
      if bool(LW_video):
        for TW, LW in zip(TW_video, LW_video):
          print(TW, LW)
          W_total['like'] += TW["like_A_Y"] - LW["like_A_Y"]
          W_total["view"] += TW["view_A_Y_T"] - LW["view_A_Y_T"]
          W_total["comment"] += TW["comment_A_Y"] - LW["comment_A_Y"]

        with conn.cursor() as cursor:      
          sql = 'INSERT INTO myapi_w_video_gap (like_A_Y, view_A_Y_T, comment_A_Y, P_key_id) VALUES (%s, %s, %s, %s)'
          cursor.execute(sql, (W_total['like'], W_total['view'] , W_total['comment'], key))
          conn.commit()
          print(cursor.lastrowid)

      TM_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(month=month).values("like_A_Y", "view_A_Y_T","comment_A_Y")
      LM_video = Video.objects.filter(P_key_id=key).filter(year=year).filter(month=month-1).values("like_A_Y", "view_A_Y_T","comment_A_Y")

      M_total = {'like':0 , 'view':0, 'comment':0}
      if bool(LM_video):
        for TM, LM in zip(TM_video, LM_video):
          print(TM, LM)
          W_total['like'] += TM["like_A_Y"] - LM["like_A_Y"]
          W_total["view"] += TM["view_A_Y_T"] - LM["view_A_Y_T"]
          W_total["comment"] += TM["comment_A_Y"] - LM["comment_A_Y"]
        
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_m_video_gap (like_A_Y, view_A_Y_T, comment_A_Y, P_key_id) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (M_total['like'], M_total['view'] , M_total['comment'], key))
            conn.commit()
            print(cursor.lastrowid)

    conn.close()