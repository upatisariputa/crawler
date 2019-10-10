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

user_ids = ['168938045', '182559117', '83422517', '263693220', '153905127', '175778772', '163472195', '261562512', '202981245', '176675885', '134532665', '189050777', '180232428', '413213644', '257352359', '240097703', '102413421', '416869407', '137953607', '207028480', '198284521', '417901095', '169883918', '417347230', '250574469', '196659347', '139397868', '196204927', '89675073', '417352747', '257685747', '209027786', '400170298', '182787083', '249168587', '262440314', '233091071', '241865606', '414573157', '184061599', '174166736', '405889189', '239773181', '421691367', '138650112', '189571500', '138473231', '236812424', '257078860', '419795496', '184538928', '418584751', '157413350', '196020104', '118929389', '165401883', '105559000', '125395014', '84794623', '224051696', '171610365', '146178249', '244047094', '138019362', '137432936', '254553750', '192726277', '117796960', '424648499', '263727220', '278845201', '149786840', '216983257', '403163827', '169529771', '197596757', '153605386', '419622106', '420088154', '161892618', '139616704', '405744903', '152064539', '175438165', '433470969', '192078267', '173101450', '206652989', '132530460', '139053470', '406600067', '206897848', '171964088', '428826125', '420761854', '183781398', '412064173', '158277639', '137814918', '217288881']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet8')

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