import pandas as pd
from flask import Flask, render_template
import pandas
import pymysql

app = Flask(__name__)

def insertSiteCount(page,cnt):
    juso_db = pymysql.connect(
        user='sunny',
        passwd='Sunhee602!',
        host='krk4ofltp00132',
        db='new_schema',
        charset='utf8'
    )
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE dailycount SET day='"+page+"',count='"+cnt+"' where day='"+page+"'"
    cursor.execute(sql)
    juso_db.commit()
    juso_db.close()
    cursor.close()
def getData(page):
    juso_db = pymysql.connect(
        user='sunny',
        passwd='Sunhee602!',
        host='krk4ofltp00132',
        db='new_schema',
        charset='utf8'
    )
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM dailycount "
    cursor.execute(sql)
    result = cursor.fetchall()
    countDF = pd.DataFrame(result)
    main = countDF[countDF['day'] == page]
    countR=int(main['count'])
    return countR

@app.route('/')
def home():
    juso_db = pymysql.connect(
        user='sunny',
        passwd='Sunhee602!',
        host='krk4ofltp00132',
        db='new_schema',
        charset='utf8'
    )
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM dailycount "
    cursor.execute(sql)
    result = cursor.fetchall()
    countDF = pd.DataFrame(result)
    countList = {"MAIN": 0, "cht": 0, "idx2": 0, "dff": 0, "mysql": 0}
    for index, row in countDF.iterrows():
        temp = countDF[countDF['day'] == countDF['day'][index]]
        r = int(temp['count'])
        countList[countDF['day'][index]] = r
    insertSiteCount("MAIN",str(countList['MAIN']+1))
    data = {'Task': 'Hours per Day', 'Main': countList['MAIN'], 'index2': countList['idx2'], 'DataFrame': countList['dff'],
            'MySQL': countList['mysql'], 'Chart': countList['cht']}
    return render_template('index.html', data=data)

@app.route('/index2')
def home2():
    r = getData("idx2")
    insertSiteCount("idx2", str(r + 1))
    return render_template('index2.html')

@app.route('/pandas')
def home3():
    r = getData("dff")
    insertSiteCount("dff", str(r + 1))
    df = pd.read_excel('C:/판다스실습/명단파일.xls')
    df_html = df.to_html()
    return df_html

@app.route('/df_site')
def pandasLink():
    r = getData("dff")
    insertSiteCount("dff", str(r + 1))
    df = pd.read_excel('C:/판다스실습/명단파일.xls')
    return render_template('df_site.html',  tables=[df.to_html(classes='data', header="true", index=False)])

@app.route('/mysql_test')
def sqllink():
    r = getData("mysql")
    insertSiteCount("mysql", str(r + 1))
    juso_db = pymysql.connect(
        user='sunny',
        passwd='Sunhee602!',
        host='krk4ofltp00132',
        db='new_schema',
        charset='utf8'
    )
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM sunnytest left join sec_table on badge=key_badge "
    cursor.execute(sql)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    juso_db.close()
    cursor.close()
    return render_template('mysql_test.html',  tables=[df.to_html(classes='data', header="true", index=False)])

@app.route('/chart')
def chartLink():
    r = getData("cht")
    insertSiteCount("cht", str(r + 1))
    candleData = [
        ['Mon', 20, 28, 38, 45],
        ['Tue', 31, 38, 55, 66],
        ['Wed', 50, 55, 77, 80],
        ['Thu', 77, 77, 66, 50],
        ['Fri', 68, 66, 22, 15]]
    return render_template("chart_sample.html", chartData=candleData)

if __name__ == '__main__':
    app.run(host='krk4ofltp00132', port=9874,debug=True) # debug = True는 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 인식하고 다시 시작한다.