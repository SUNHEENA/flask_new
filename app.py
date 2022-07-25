import pandas as pd
from flask import Flask, render_template
import pandas
import pymysql
import dbHandling
from flask import Flask, request
from flask.json import jsonify
from flask.templating import render_template

app = Flask(__name__, template_folder='static/FrontEnd')

def loopDataWithGoogleChart(inputList : dict):
    ##디폴트값 세트
    resultData = [['Task', 'Page Count']]
    for keyList in inputList:
        tmpList=list()
        tmpList.append(keyList)
        tmpList.append(inputList[keyList])
        resultData.append(tmpList)
    return resultData

@app.route('/')
def home():
    db = dbHandling.DB()
    countList = db.mainLogin()
    db.insertSiteCount("MAIN",str(countList['MAIN']+1))
    del db
    data = loopDataWithGoogleChart(countList)
    # data = [['Task', 'Hours per Day'],['Main', countList['MAIN']],
    #         ['index2', countList['idx2']],['DataFrame', countList['dff']],['MySQL', countList['mysql']],['Chart', countList['cht']]]
    return render_template('index.html', charData=data)

@app.route('/index2')
def home2():
    db = dbHandling.DB()
    r = db.getData("idx2")
    db.insertSiteCount("idx2", str(r + 1))
    return render_template('index2.html')

@app.route('/pandas')
def home3():
    db = dbHandling.DB()
    r = db.getData("dff")
    db.insertSiteCount("dff", str(r + 1))
    df = pd.read_excel('C:/판다스실습/명단파일.xls')
    df_html = df.to_html()
    return df_html

@app.route('/df_site')
def pandasLink():
    db = dbHandling.DB()
    r = db.getData("dff")
    db.insertSiteCount("dff", str(r + 1))
    del db
    df = pd.read_excel(r'C:/jupyter_notebook_Source/python_intermediate/im_test_문서/IM_TEST_DF1.xlsx')
    return render_template('df_site.html',  tables=[df.to_html(classes='data', header="true", index=False)])

@app.route('/mysql_test')
def sqllink():
    db = dbHandling.DB()
    r = db.getData("mysql")
    db.insertSiteCount("mysql", str(r + 1))
    juso_db = pymysql.connect(
        user='sun',
        passwd='Sunhee602!',
        host='KRK4OFLTP00357',
        db='flask_db',
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
    db = dbHandling.DB()
    r = db.getData("cht")
    db.insertSiteCount("cht", str(r + 1))
    candleData = [
        ['Mon', 20, 28, 38, 45],
        ['Tue', 31, 38, 55, 66],
        ['Wed', 50, 55, 77, 80],
        ['Thu', 77, 77, 66, 50],
        ['Fri', 68, 66, 22, 15]]
    return render_template("chart_sample.html", chartData=candleData)


@app.route('/pyscript')
def pyScriptSample():
    return render_template('pyscript.html',)

##TABLE 실습예제
@app.route('/tableUpdate')
def emp():
    db = dbHandling.DB()
    cntList = db.getSample()
    return render_template("tableTest.html", cntList=cntList)

#insert ajax 통신을 위한 구문
@app.route('/ins.ajax', methods=['POST'])
def ins_ajax():
    data = request.get_json()
    type = data['type']
    count = data['cnt']
    db = dbHandling.DB()
    cnt = db.insertSite(type,count)
    result = "success" if cnt==1 else "fail"
    return jsonify({'msg': result})

##나는 가져오는 부분
@app.route('/getallData', methods=['GET'])
def read_data():
    return jsonify({'msgReturn': 'TESTTT'})

#delete를 위한 구문
@app.route('/del.ajax', methods=['POST'])
def del_ajax():
    data = request.get_json()
    type = data['type']
    db = dbHandling.DB()
    cnt = db.deleteType(type)
    result = "success" if cnt==1 else "fail"
    return jsonify({'msg': result})

##get 하는 주소
@app.route('/getTest')
def getterSetter():
    db = dbHandling.DB()
    cntList = db.getSample()
    return jsonify(cntList)

if __name__ == '__main__':
    app.run(host='KRK4OFLTP00357', port=9874,debug=True) # debug = True는 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 인식하고 다시 시작한다.