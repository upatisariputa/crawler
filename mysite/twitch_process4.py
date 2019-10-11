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

user_ids = ['139260229', '242074857', '124316825', '138822997', '270847429', '162859176', '226722120', '138198516', '195480364', '182405231', '164462662', '138386672', '138094321', '159714478', '205767052', '180529010', '203972891', '143861165', '236543759', '218427894', '159396431', '189552956', '219209230', '237271861', '148088486', '189876327', '169533383', '134069248', '144082255', '190212028', '139234421', '172552749', '238591630', '150641916', '118204488', '211471778', '138997208', '103963157', '137987280', '139718802', '166138842', '236324189', '247565756', '266790309', '138131810', '174649097', '139417491', '275644615', '150406440', '224047720', '259622203', '166485593', '192362794', '257926332', '250639350', '150039837', '156735529', '211521839', '189168209', '196073646', '152437743', '180427299', '445820187', '116640165', '181352920', '160989002', '126881929', '158976643', '212948078', '140060967', '64067566', '403994675', '279435561', '203908691', '189863169', '146898628', '138051253', '194540326', '44556441', '273971135', '218403838', '233544499', '410559528', '188784707', '170979045', '183548508', '170706307', '145794809', '275635599', '265268547', '160176441', '163745628', '244467801', '157412649', '163014099', '198713808', '145562459', '116816258', '231580741', '169007499']

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
    p_keys = Platform.objects.filter(P_name='twitch').values('P_key')[300:400]
    
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