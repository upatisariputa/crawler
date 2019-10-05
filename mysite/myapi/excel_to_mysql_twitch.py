import xlrd
import pymysql.cursors

book = xlrd.open_workbook('twitch.xlsx')
sheet = book.sheet_by_name('시트 1')

conn = pymysql.connect(host='localhost', user='root',
                       password=None, db='ilio', charset='utf8mb4')

for r in range(1, sheet.nrows):
    P_userkey = str(sheet.cell(r, 0).value)
    P_url = sheet.cell(r, 1).value
    P_name = sheet.cell(r, 2).value

    with conn.cursor() as cursor:
        sql = 'INSERT INTO myapi_platform (P_url, P_userkey, P_name) VALUES (%s, %s, %s)'
        cursor.execute(sql, (P_url, P_userkey, P_name))
    conn.commit()
