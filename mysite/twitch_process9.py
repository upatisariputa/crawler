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

user_ids = ['261623877', '137952746', '139182425', '429055679', '140133865', '194007102', '245988762', '137833091', '421740672', '144877593', '404167064', '403787873', '151551848', '265224135', '138287817', '256690793', '186449802', '151703610', '250041386', '173913885', '232376547', '160517115', '400969279', '177329360', '147965553', '186418858', '140526293', '237583706', '197281335', '190450337', '151792360', '87452695', '138982718', '133268113', '138112139', '421424844', '276803962', '246183631', '147257710', '254576830', '186024100', '427609725', '401822139', '404173604', '267499375', '144757892', '188666346', '140248766', '177659426', '158943745', '215577048', '265430108', '164093633', '401173550', '412610018', '419972813', '432235268', '165009288', '418853755', '181776929', '197984477', '405196352', '267236268', '189706769', '231340452', '237570548', '129530787', '422869029', '265855439', '223819316', '405369467', '262451416', '274865124', '433183417', '412368402', '427300788', '433091390', '433314700', '148057505', '248122367', '433497796', '135344599', '276586271', '255238454', '103989366', '273272249', '205145331', '237846471', '217014177', '138335148', '401496596', '138304078', '175341964', '247404203', '137600946', '139050149', '142890659', '137906785', '435540897', '191841708']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet9')

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