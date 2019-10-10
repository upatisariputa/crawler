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

user_ids = ['239336234', '239476460', '432387042', '250168149', '132252562', '178413249', '187090662', '138127092', '263734595', '412825661', '224524220', '158253328', '407415033', '196510444', '198832788', '431832981', '426152342', '241881550', '248134382', '416453629', '257701649', '160724122', '413904984', '208456730', '442432168', '177683356', '179623595', '437437203', '165891534', '429144154', '168278158', '81478902', '201579969', '166604396', '427239505', '401086799', '424252846', '238555307', '171497333', '416919773', '128390932', '270228387', '415635612', '420333709', '127611509', '214408882', '437884924', '160101118', '182002718', '219045201', '202190437', '246600066', '144957003', '122323361', '205206238', '155637966', '128635717', '442709328', '421461070', '416425730', '272791773', '269589407', '170064018', '164772369', '277715491', '85534873', '177973076', '148061879', '191587723', '432386695', '403759679', '441996250', '149876828', '432609988', '432417191', '134604443', '446523866', '445841701', '146229748', '177319240', '191961745', '137613449', '159717496', '228600337', '171241791', '184988006', '247366568', '101589700', '137472204', '445562856', '431054664', '406165837', '177214992', '152928100', '166788981', '148098488', '143947234', '260936637', '236113110', '441033728']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet12')

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