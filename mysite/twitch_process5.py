import pymysql.cursors, requests, time, re, xlrd, os
from django.db.models import Sum
from time import localtime, strftime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from myapi.models import Platform, Subscribe, User_info, Video
from multiprocessing import Pool
headers = {'Client-ID': 'orr8549md8anh4puxs904dyswcgfb3',
           'referer': 'https://twitch.tv'}
conn = pymysql.connect(host='localhost', user='root',
                       password=None, db='ilio', charset='utf8mb4')
user_ids = ['425968734', '267512124', '169206387', '254028851', '410268408', '194293413', '179811902', '150048126', '435324919', '437601547', '265829143', '148416060', '149234692', '264408392', '152719759', '424035946', '152842341', '137798768', '261538378', '403148573', '431864116', '434459669', '240967419', '138910332', '457636953', '193858736', '167088233', '162619797', '188282850', '247890689', '167579290', '168697286', '195485487', '144312134', '233433249', '443561931', '277623466', '445016474', '414935710', '217516998', '138290417', '152707772', '215795288', '453709598', '454722486', '250613867', '182114978', '272555753', '160065615', '152723467', '157308033', '160547692', '186309208', '138527621', '137968227', '231783921', '142671030', '160677135', '230484610', '137640527', '140175340', '135501610', '183012826', '178876724', '141630000', '150521673', '183775106', '147308412', '152295931', '185050876', '160807533', '175232047', '195324562', '192387083', '163683885', '140662316', '188786546', '138229898', '147098912', '175979971', '195879005', '140244490', '139239197', '194316027', '240468265', '247099914', '207719948', '208866887', '218257429', '137877158', '464966847', '194707353', '196181992', '135179343', '183748267', '184489331', '86403736', '160349660', '163469195', '139430811']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)
createtime = strftime('%Y-%m-%d', localtime())

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet5')
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

def combine_id_p_key(id_list):
    p_keys = []
    combined = []
    r = Platform.objects.values('P_key')
    for keys in r:
        p_keys.append(keys['P_key'])
    for key in p_keys:
        combined.append([key])
    
    i = 0
    
    for id in id_list:
        combined[i].append(id)
        i += 1
    
    lists = [combined[x:x+10] for x in range(0, len(combined), 10)]
    return lists

def get_user_info(id_list):
    r = requests.get('https://api.twitch.tv/helix/users?id=' +
                    id_list[1], headers=headers)
    user = r.json()
    image_url = user['data'][0]['profile_image_url']
    user_name = user['data'][0]['display_name']
    user_info = user['data'][0]['description']
    platform_key = id_list[0]
    
    if bool(User_info.objects.filter(P_key = platform_key)):
        with conn.cursor() as cursor:      
            sql = 'UPDATE myapi_user_info SET (U_name, U_img, U_info, U_sudate) WHERE (P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (user_name, image_url, user_info, 'null', platform_key))
        conn.commit()
        print(platform_key)
    else:
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (user_name, image_url, user_info, 'null', platform_key))
        conn.commit()
        print(platform_key)
   
    time.sleep(2)
    
def get_followers_info(id_list):
    r = requests.get(
        'https://api.twitch.tv/helix/users/follows?to_id=' + id_list[1] + '', headers=headers)
    followers = r.json()
    number_of_followers = followers['total']
    platform_key = id_list[0]
    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_subscribe (created_at, S_count, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, ('null', number_of_followers, year, month, week, day, platform_key))
    conn.commit()
    time.sleep(2)
    TDsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(month=month).filter(day=day).values('S_count')
    YDsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(month=month).filter(day=day-1).values('S_count')
    
    if len(TDsub) >= 1 and len(YDsub) >= 1:
        D_sub = TDsub[0]['S_count']-YDsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_d_sub_gap (sub_count, P_key_id) VALUES (%s, %s)'
            cursor.execute(sql, (D_sub, platform_key))
        conn.commit()
    TWsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(week=month).aggregate(total=Sum('S_count'))
    LWsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(week=month-1).aggregate(total=Sum('S_count'))
    if bool(TWsub['total']) and bool(LWsub['total']) :
        W_sub = TWsub[0]['S_count']-LWsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_w_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (W_sub, platform_key))
        conn.commit()
    
    TMsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(month=month).aggregate(total=Sum('S_count'))
    LMsub = Subscribe.objects.filter(P_key_id=platform_key).filter(year=year).filter(month=month-1).aggregate(total=Sum('S_count'))
    
    if bool(TMsub['total']) and bool(LMsub['total']) :
        M_sub = TMsub[0]['S_count']-LMsub[0]['S_count']
        with conn.cursor() as cursor:      
            sql = 'INSERT INTO myapi_m_sub_gap (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (M_sub, platform_key))
        conn.commit()
    time.sleep(2)

def get_video_info(id_list):
    videos = [] 
    platform_key = id_list[0]
    r = requests.get(
        'https://api.twitch.tv/helix/videos?user_id=' + id_list[1] + '&first=100', headers=headers)
    r = r.json()
    pagination_cursor = r['pagination']['cursor']
    videos += r['data']
    while 1:
        r = requests.get(
            'https://api.twitch.tv/helix/videos?user_id=' + id_list[1] + '&first=100&after=' + pagination_cursor, headers=headers)
        r = r.json()
        videos += r['data']
        if r['pagination'] != {}:
            pagination_cursor = r['pagination']['cursor']
        else:
            break
    
    for video in videos:
        title = video['title']
        update_date = video['published_at']
        view_count = video['view_count']
        with conn.cursor() as cursor:
            sql = 'INSERT INTO myapi_video (V_name, V_upload, like_A_Y, dislike_Y, view_A_Y_T, comment_A_Y, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (title, update_date, 'null', 'null', view_count, 'null', year, month, week, day, platform_key))
    conn.commit()
    time.sleep(2)


def get_total(id_list):
    platform_key = id_list[0]
    t_view_cnt = Video.objects.filter(P_key_id=platform_key).aggregate(total=Sum('T_view_count'))
    with conn.cursor() as cursor:      
        sql = 'INSERT INTO myapi_total (T_like_count_A_Y, T_unlike_count_Y, T_view_count_A_Y_T, T_update, P_key_id) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, ("null", "null", t_view_cnt, createtime, platform_key))
        conn.commit()

def get_info(id_list):
    get_user_info(id_list)
    time.sleep(2)
    get_followers_info(id_list)
    time.sleep(2)
    get_video_info(id_list)
    time.sleep(2)
    get_total(id_list)


def multiprocessing():
    pool = Pool()
    pool.map_async(get_info, combined_list)
    pool.close()
    pool.join()

if __name__ == '__main__':
    import time
    get_platform_info()
    lists = combine_id_p_key(user_ids)
    for combined_list in lists:
        multiprocessing()
    
    print('task completed')