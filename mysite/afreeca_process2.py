import os, json, pymysql, time, xlrd
from urllib.request import Request, urlopen
from django.db.models import Sum
from time import localtime, strftime

#순서 바꾸면 안된다. 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()
from myapi.models import Platform, Subscribe, User_info, Video
from multiprocessing import Pool

# 현제 년,월,일,주
time = time.localtime()
year = time.tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)
createtime = strftime('%Y-%m-%d', localtime())
        

# Platform table 에서 값을 가져온다. 

def get_platform_info():
    book = xlrd.open_workbook('afreeca (1).xlsx')
    sheet = book.sheet_by_name('afreeca2')

    conn = pymysql.connect(host='localhost', user='root',
                           password=None, db='ilio', charset='utf8mb4')

    for r in range(0, sheet.nrows):
        P_userkey = str(sheet.cell(r, 0).value)
        P_url = sheet.cell(r, 1).value
        P_name = sheet.cell(r, 2).value

        with conn.cursor() as cursor:
            sql = 'INSERT INTO myapi_platform (P_url, P_userkey, P_name) VALUES (%s, %s, %s)'
            cursor.execute(sql, (P_url, P_userkey, P_name))
        conn.commit()
    print('data migration complete')



def get_info(p):
    conn = pymysql.connect(host='localhost',
                            user='root',
                            password=None,
                            db='ilio',
                            charset='utf8mb4')
    name = p['P_url'].replace('http://bj.afreecatv.com/', '')
#  print(i['P_url'].replace(r'(/(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}\//gi)', ')) 정규 표현식 사용법 찾아보기
    # 팬클럽, 서포터  수 정보
    URL = 'http://bjapi.afreecatv.com/api/'+ name +'/station/detail'
    response = urlopen(URL)
    fanclub = json.load(response)['count']

    # BJ 정보 , 이름, 썸네일, 구독 ,애청자
    URL = 'http://bjapi.afreecatv.com/api/'+ name +'/station'
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    bj_info = json.load(response)


    img = bj_info['profile_image']
    introduce = bj_info['station']['display']['profile_text']
    name = bj_info['station']['user_nick']
    fav_fan = bj_info['station']['upd']['fan_cnt']
    t_ok_cnt = bj_info['station']['upd']['total_ok_cnt']
    t_view_cnt = bj_info['station']['upd']['total_view_cnt']
    signup = bj_info['station']['jointime']

    # print(img, '\n', introduce, '\n', name, '\n', '\n', fav_fan, '\n', signup)

    #구독 정보
    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_subscribe (created_at, S_count, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (createtime, fav_fan, year, month, week, day, p['P_key']))
    conn.commit()
    print('entering')

    time.sleep(2)

    #유저 정보
    if bool(User_info.objects.filter(P_key=p['P_key'])):
        with conn.cursor() as cursor:      
            sql = 'UPDATE myapi_user_info SET U_name=%s, U_img=%s, U_info=%s WHERE P_key_id=%s'
            cursor.execute(sql, (name, img, introduce, p['P_key']))
        conn.commit()
        print('entering')

    else:
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (name, img, introduce, signup, p['P_key']))
        conn.commit()
        print('entering')
    
    time.sleep(2)
#총합
    with conn.cursor() as cursor:      
        sql = 'INSERT INTO myapi_total (T_like_count, T_unlike_count, T_view_count, T_update, P_key_id) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (t_ok_cnt, 0, t_view_cnt, createtime ,p['P_key']))
    conn.commit()
    print('entering')

    time.sleep(2)
    #일간 차
    TDsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(month=month).filter(day=day).values('S_count')
    YDsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(month=month).filter(day=day-1).values('S_count')
    
    if len(TDsub) >= 1 and len(YDsub) >= 1:
        D_sub = TDsub[0]['S_count']-YDsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_d_sub_gap (sub_count, P_key_id) VALUES (%s, %s)'
            cursor.execute(sql, (D_sub, p['P_key']))
        conn.commit()
        print('entering')
    
    time.sleep(2)

    #주간 차
    TWsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(week=month).aggregate(total=Sum('S_count'))
    LWsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(week=month-1).aggregate(total=Sum('S_count'))

    if bool(TWsub['total']) and bool(LWsub['total']) :
        W_sub = TWsub[0]['S_count']-LWsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_w_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (W_sub, p['P_key']))
        conn.commit()
        print('entering')

    time.sleep(2)

    #월간 차
    TMsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(month=month).aggregate(total=Sum('S_count'))
    LMsub = Subscribe.objects.filter(P_key_id=p['P_key']).filter(year=year).filter(month=month-1).aggregate(total=Sum('S_count'))
    
    if bool(TMsub['total']) and bool(LMsub['total']) :
        M_sub = TMsub[0]['S_count']-LMsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_m_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (M_sub, p['P_key']))
        conn.commit()
        print('entering')

    time.sleep(2)

    name = p['P_url'].replace("http://bj.afreecatv.com/", "")
    conn = pymysql.connect(host='localhost',
                          user='root',
                          password=None,
                          db='ilio',
                          charset='utf8mb4')
    URL = "http://bjapi.afreecatv.com/api/"+name+"/vods"
    response = urlopen(URL)
    page = json.load(response)["meta"]["last_page"]+1
    key = p['P_key']
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
            print('entering')
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
            print('entering')
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
          print('entering')
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

    conn.close()

def multiprocessing():
    pool = Pool()
    pool.map_async(get_info, p_key)
    pool.close()
    pool.join()

if __name__ == '__main__':
    import time
    get_platform_info()
    p_key = []
    p_key = Platform.objects.filter(P_name='Afreeca').values('P_key','P_userkey','P_url','P_name')[101:202]

    multiprocessing()

    print('task completed')