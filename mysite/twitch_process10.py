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

user_ids = ['154813896', '268714924', '268059905', '166810763', '140579996', '186348742', '425689986', '275431890', '213195690', '219850189', '280480523', '277154335', '273399714', '224396536', '144645178', '262645565', '407269437', '242939402', '118177511', '223827133', '167419985', '258147715', '203690678', '405891339', '179032436', '432802969', '257337034', '431099756', '162078233', '107056983', '168426624', '150590353', '428382974', '141416065', '203701034', '279566895', '153497051', '416866512', '79157656', '129797992', '219499247', '133670112', '194577822', '133861352', '171477690', '423681832', '265855509', '433471983', '426353015', '196534554', '173319589', '206718950', '160301738', '274441932', '189362622', '159004385', '177079953', '154321527', '400362772', '412778070', '413441387', '137913993', '265062514', '259694951', '264405197', '236102264', '133677373', '424541127', '258696064', '155247648', '409442178', '431760807', '181217198', '191832014', '142482328', '238549800', '162472520', '137104290', '70939763', '153681664', '417174773', '431179047', '404062455', '428796660', '235122143', '137623860', '219405917', '197097403', '194666447', '424717679', '410604078', '132195222', '152219386', '173132149', '170074588', '153561820', '147086897', '439580521', '195574036', '425563603']

time = time.localtime()
year = time. tm_year
month = time.tm_mon
day = time.tm_mday
week = int(time.tm_yday/7)

def get_platform_info():
    book = xlrd.open_workbook('twitch.xlsx')
    sheet = book.sheet_by_name('Sheet10')

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