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

user_ids = ['213244638', '149702330', '147242105', '139447097', '137808437', '233708175', '450518514', '137334715', '196010921', '173366410', '181276195', '156795005', '192387083', '234900909', '151695731', '180934252', '228611812', '139824322', '165236343', '187553635', '154514562', '187400344', '194046640', '261038919', '214650306', '128384349', '161744909', '157084502', '139441653', '138555858', '243815774', '263443071', '204478940', '215186790', '133684560', '148492670', '93228130', '208423581', '246100973', '138042768', '188502310', '182270538', '146634459', '148202573', '249999252', '134028817', '149986673', '217011592', '158374756', '145046857', '150846309', '131579881', '175056259', '175651814', '238494371', '263469464', '158122035', '268733352', '190682563', '212950722', '195035997', '233231746', '141729119', '142488135', '147918001', '150218244', '139045318', '137797349', '188722893', '154423377', '172279729', '205043585', '157294109', '133045915', '253114553', '232779448', '178905070', '245880529', '172475722', '198103540', '187389453', '215345525', '180416432', '280288480', '232397581', '144083287', '139433619', '137561429', '153878524', '236759235', '84995253', '236278201', '181777943', '135223638', '51230738', '203435847', '181889983', '197454974', '227154776', '198288245']

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
    p_keys = Platform.objects.filter(P_name='twitch').values('P_key')[100:200]
    
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