import os, json, pymysql, time
from urllib.request import Request, urlopen
from django.db.models import Sum
from time import localtime, strftime

#순서 바꾸면 안된다. 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()
from myapi.models import Platform, Subscribe, User_info

# 현제 년,월,일,주
time = time.localtime()
year = time.tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)
createtime = strftime('%Y-%m-%d', localtime())

# Platform table 에서 값을 가져온다. 
p_key = []
p_key = Platform.objects.filter(P_name='afreeca').values('P_key','P_userkey','P_url','P_name')

for i in p_key:
    name = i['P_url'].replace("http://bj.afreecatv.com/", "")
#  print(i['P_url'].replace(r'(/(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}\//gi)', "")) 정규 표현식 사용법 찾아보기

    # 팬클럽, 서포터  수 정보
    URL = "http://bjapi.afreecatv.com/api/"+name+"/station/detail"
    response = urlopen(URL)
    fanclub = json.load(response)["count"]

    # BJ 정보 , 이름, 썸네일, 구독 ,애청자
    URL = "http://bjapi.afreecatv.com/api/"+ name +"/station"
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    bj_info = json.load(response)


    img = bj_info["profile_image"]
    introduce = bj_info["station"]["display"]["profile_text"]
    name = bj_info["station"]["user_nick"]
    fav_fan = bj_info["station"]["upd"]["fan_cnt"]
    t_ok_cnt = bj_info["station"]["upd"]["total_ok_cnt"]
    t_view_cnt = bj_info["station"]["upd"]["total_view_cnt"]
    signup = bj_info["station"]["jointime"]

    # print(img, "\n", introduce, "\n", name, "\n", "\n", fav_fan, "\n", signup)

    conn = pymysql.connect(host='localhost',
                          user='root',
                          password=None,
                          db='ilio',
                          charset='utf8mb4')
    
    #구독 정보
    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_subscribe (created_at, S_count, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (createtime, fav_fan, year, month, week, day, i['P_key']))
        conn.commit()
        print(cursor.lastrowid)

    #유저 정보
    if bool(User_info.objects.filter(P_key=i['P_key'])):
      with conn.cursor() as cursor:      
          sql = 'UPDATE myapi_user_info SET U_name=%s, U_img=%s, U_info=%s WHERE P_key_id=%s'
          cursor.execute(sql, (name, img, introduce, i['P_key']))
          conn.commit()
          print(cursor.lastrowid)

    else:
      with conn.cursor() as cursor:      
          sql = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
          cursor.execute(sql, (name, img, introduce, signup, i['P_key']))
          conn.commit()
          print(cursor.lastrowid)
    
  #총합
    with conn.cursor() as cursor:      
        sql = 'INSERT INTO myapi_total (T_like_count, T_unlike_count, T_view_count, T_update, P_key_id) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (t_ok_cnt, 0, t_view_cnt, createtime ,i['P_key']))
        conn.commit()
        print(cursor.lastrowid)

    #일간 차
    TDsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(month=month).filter(day=day).values('S_count')
    YDsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(month=month).filter(day=day-1).values('S_count')
    
    if len(TDsub) >= 1 and len(YDsub) >= 1:
      D_sub = TDsub[0]['S_count']-YDsub[0]['S_count']
      with conn.cursor() as cursor:      
          sql = 'INSERT INTO myapi_d_sub_gap (sub_count, P_key_id) VALUES (%s, %s)'
          cursor.execute(sql, (D_sub, i['P_key']))
          conn.commit()
          print(cursor.lastrowid)
    
    #주간 차
    TWsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(week=month).aggregate(total=Sum('S_count'))
    LWsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(week=month-1).aggregate(total=Sum('S_count'))

    if bool(TWsub['total']) and bool(LWsub['total']) :
      W_sub = TWsub[0]['S_count']-LWsub[0]['S_count']
      with conn.cursor() as cursor:      
          sql = 'INSERT INTO myapi_w_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
          cursor.execute(sql, (W_sub, i['P_key']))
          conn.commit()
          print(cursor.lastrowid)

    #월간 차
    TMsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(month=month).aggregate(total=Sum('S_count'))
    LMsub = Subscribe.objects.filter(P_key_id=i['P_key']).filter(year=year).filter(month=month-1).aggregate(total=Sum('S_count'))
    
    if bool(TMsub['total']) and bool(LMsub['total']) :
      M_sub = TMsub[0]['S_count']-LMsub[0]['S_count']
      with conn.cursor() as cursor:      
          sql = 'INSERT INTO myapi_m_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
          cursor.execute(sql, (M_sub, i['P_key']))
          conn.commit()
          print(cursor.lastrowid)

    conn.close()