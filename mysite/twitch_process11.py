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

user_ids = ['195634482', '138775351', '400763835', '188148588', '134021718', '263223977', '161873222', '408533520', '278103679', '403601785', '157694596', '222823240', '436260092', '149061865', '430575842', '402605781', '404350187', '179774869', '160537425', '184602534', '42848761', '271851344', '267825977', '232541746', '270836749', '189838998', '406986372', '189556936', '268276100', '176355694', '183688276', '253352366', '157144067', '185902966', '266063913', '141121593', '153156560', '441835960', '437282335', '258091327', '432575205', '421929973', '171092875', '435286026', '422066867', '90328215', '266762505', '278878199', '214670813', '429513185', '161320628', '150747651', '405485268', '413478237', '401836847', '152964747', '189408382', '137803146', '134352671', '438207129', '160166535', '52007643', '165833857', '165269647', '433142289', '175045528', '128749648', '153978848', '252312595', '257657683', '277733169', '413597335', '280212666', '425976524', '241003262', '412864672', '422126939', '138202320', '430490232', '177346153', '176856170', '427468711', '419179541', '170896864', '411819151', '415085970', '172505143', '440119350', '131396124', '146819453', '261909821', '185299679', '427318700', '230245537', '157144690', '239440830', '158059431', '243954349', '166746163', '255207110']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)
createtime = strftime('%Y-%m-%d', localtime())

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Main')
    conn = pymysql.connect(host='localhost', user='root',
                           password=None, db='ilio', charset='utf8mb4')
    for r in range(0, sheet.nrows):
        P_userkey = str(sheet.cell(r, 0).value)
        P_url = sheet.cell(r, 1).value
        P_name = sheet.cell(r, 2).value
        if bool(Platform.objects.filter(P_userkey=P_userkey)):
            with conn.cursor() as cursor:
                sql = 'UPDATE myapi_platform SET P_url=%s, P_name=%s WHERE P_userkey=%s'
                cursor.execute(sql, (P_url, P_name, P_userkey)) 
        else :
            with conn.cursor() as cursor:
                sql = 'INSERT INTO myapi_platform (P_url, P_userkey, P_name) VALUES (%s, %s, %s)'
                cursor.execute(sql, (P_url, P_userkey, P_name))
            conn.commit()
    print('data migration complete')

def combine_id_p_key(id_list):
    p_keys = []
    p_keys = Platform.objects.filter(P_name='twitch').values('P_key')[1000:1100]
    
    combined = []
    
    for key in p_keys:
        combined.append([key['P_key']])
    
    i = 0
    
    for id in id_list:
        combined[i].append(id)
        i += 1
    
    lists = [combined[x:x+10] for x in range(0, len(combined), 10)]
    return lists

def get_user_info(id_list):
    try:
        r = requests.get('https://api.twitch.tv/helix/users?id=' +
                        id_list[1], timeout=5, headers=headers)
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

        else:
            with conn.cursor() as cursor:      
                sql = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql, (user_name, image_url, user_info, 'null', platform_key))
            conn.commit()
        time.sleep(2)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    
def get_followers_info(id_list):
    try:
        r = requests.get(
            'https://api.twitch.tv/helix/users/follows?to_id=' + id_list[1] + '', timeout=5, headers=headers)
        followers = r.json()
        number_of_followers = followers['total']
        platform_key = id_list[0]
        with conn.cursor() as cursor:
            sql = 'INSERT INTO myapi_subscribe (created_at, S_count, year, month, week, day, P_key_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, ('null', number_of_followers, year, month, week, day, platform_key))
        conn.commit()

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
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def get_video_info(id_list):
    try:
        videos = [] 
        platform_key = id_list[0]
        r = requests.get(
            'https://api.twitch.tv/helix/videos?user_id=' + id_list[1] + '&first=100', timeout=5, headers=headers)
        r = r.json()
        pagination_cursor = r['pagination']['cursor']
        videos += r['data']
        while 1:
            r = requests.get(
                'https://api.twitch.tv/helix/videos?user_id=' + id_list[1] + '&first=100&after=' + pagination_cursor, timeout=5, headers=headers)
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
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def get_info(id_list):
    get_user_info(id_list)
    time.sleep(2)
    get_followers_info(id_list)
    time.sleep(2)
    get_video_info(id_list)

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
    conn.close()