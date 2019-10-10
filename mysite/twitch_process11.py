import pymysql.cursors
import requests
import time
import re
import xlrd
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from myapi.models import Platform
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

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet11')

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
    with conn.cursor() as cursor:
        query = 'INSERT INTO myapi_user_info (U_name, U_img, U_info, U_sudate, P_key_id) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(query, (user_name, image_url, user_info, 'null', platform_key))
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

def get_info(id_list):
    get_user_info(id_list)
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