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

user_ids = ['231386065', '138531769', '242137321', '140668752', '258942488', '207455842', '138222558', '196053235', '266457537', '183562796', '277754497', '269132402', '137647241', '198646065', '266041504', '248042118', '139054497', '164079660', '149605187', '248158421', '138542600', '157505700', '160080149', '228008443', '137381625', '141751420', '156946395', '193934608', '173756073', '247104109', '152371112', '105416974', '167112608', '149307487', '167184519', '405431741', '137498697', '178722705', '278420353', '137471348', '268024226', '195065545', '420157307', '181522504', '168802338', '215547251', '266833425', '404191479', '140383069', '175445419', '148505696', '203366403', '411172389', '403192252', '238745501', '414963418', '180417777', '277701382', '276078820', '137952370', '138220297', '161513899', '139725330', '147420839', '152453460', '238372548', '273557271', '196023489', '160295902', '416906042', '141837379', '169821502', '148775241', '408885215', '275956168', '242064834', '173766732', '271097307', '137906426', '150391390', '131654444', '416463937', '79788991', '175673197', '181064501', '266087900', '138728503', '196908461', '265851134', '137553239', '245481676', '144360256', '155591286', '404400610', '213679485', '401479342', '133247892', '404344086', '245278200', '168432480']

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
    p_keys = Platform.objects.filter(P_name='twitch').values('P_key')[600:700]
    
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