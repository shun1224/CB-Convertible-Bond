from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask.logging import create_logger
import sqlite3
import pack.modu as lib
import csv

app = Flask(__name__)          # __name__ 代表目前執行的模組
app.debug = True               # 當程式碼有變動，網頁會重載，預設為關閉
app.secret_key = "20220102"
log = create_logger(app)       # 定義一個儲存 log 的物件
appTitle = '可轉債分析系統'         # 網頁標題
recs = []

@app.route("/", methods=['GET', 'POST'])
def tryout():
    return render_template('tryout.html', title=appTitle, recs=recs)

@app.route("/main", methods=['GET', 'POST'])
def main():
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        return render_template('main.html', title=appTitle, recs=recs)

def chkLogin(uid, pwd):
    with open('pass.csv', mode='r', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader, None)                                 # 跳過標題
        passDict = {rows[0]:rows[1] for rows in csvReader}    # 列表生成式
        if not (uid in passDict and pwd in passDict[uid]):
            return False
        else:
            return True

def chkSessionOK():
    if not session.get('username'):  # 若session不存在，則導向回首頁
        return False
    else:
        return True

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not chkLogin(username.strip(), password.strip()):
            info = '=>帳密錯誤'
            log.warning(info)
            flash(info)
            return redirect(url_for('login'))
        else:
            session['username'] = username  # 設置session
            lib.vipDB(username)
            return redirect(url_for('main'))
    else:
        return render_template('login.html', title=appTitle)

@app.route("/logout")
def logout():
    global recs
    recs = []
    session['username'] = False  # 刪除session
    info = '=>已登出'
    log.warning(info)
    flash(info)
    return redirect(url_for('tryout'))

@app.route("/low_risk")
def low_risk(): #低風險名單
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        try:
            if vip_name=='shun' or vip_name=='jack':
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(f"select * from {vip_name} where (擔保銀行 like '%聯保%' or 擔保銀行 like '%銀%' or 擔保銀行 like '%1%' or 擔保銀行 like '%2%'\
                or 擔保銀行 like '%2%' or 擔保銀行 like '%3%'or 擔保銀行 like '%4%' or 擔保銀行 like '%5%') and (最新CB收盤價 not like '%已全部轉換%' and 最新CB收盤價 not like '%無成交%') \
                and(轉換比例 < 30) ORDER BY 最新CB收盤價 ASC")
                recs = cursor.fetchall()
                info = '=> 有銀行擔保 或 TCRI信用評等 < 5 的 , 加上價格接近合理安全的標的'
            else:
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute("select * from data where (擔保銀行 like '%聯保%' or 擔保銀行 like '%銀%' or 擔保銀行 like '%1%' or 擔保銀行 like '%2%'\
                or 擔保銀行 like '%2%' or 擔保銀行 like '%3%'or 擔保銀行 like '%4%' or 擔保銀行 like '%5%') and (最新CB收盤價 not like '%已全部轉換%' and 最新CB收盤價 not like '%無成交%') \
                and(轉換比例 < 30) ORDER BY 最新CB收盤價 ASC")
                recs = cursor.fetchall()
                info = '=> 有銀行擔保 或 TCRI信用評等 < 5 的 , 加上價格接近合理安全的標的'
        except:
            info = "=>顯示清單失敗"
        conn.commit()
        conn.close()
        log.warning(info)
        flash(info)
        return redirect(url_for('main'))

@app.route("/importData")
def importData(): #更新資料
    global recs
    recs = []
    vip_name=session.get('username')
    if vip_name=='shun' or vip_name=='jack':
        try:
            lib.r1(vip_name)
            info = "更新成功"
        except:
            info = "=>更新失敗"
        log.warning(info)
        flash(info)
        return redirect(url_for('main'))
    else:
        try:
            lib.r1(vip_name)
            info = "更新成功"
        except:
            info = "=>更新失敗"
        log.warning(info)
        flash(info)
        return redirect(url_for('tryout'))

@app.route("/qryTable")
def qryTable(): #可轉債清單列表
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        try:
            conn = sqlite3.connect('mydb.db')
            cursor = conn.execute("select * from data")
            recs = cursor.fetchall()
            conn.commit()
            conn.close()
        except:
            info = "=>顯示清單失敗"
            log.warning(info)
            flash(info)
        return redirect(url_for('tryout'))
    else:
        try:
            if vip_name=='shun' or vip_name=='jack':
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(f"select * from {vip_name}")
                recs = cursor.fetchall()
            else:
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute("select * from data")
                recs = cursor.fetchall()
            conn.commit()
            conn.close()
        except:
            info = "=>顯示清單失敗"
            log.warning(info)
            flash(info)
        return redirect(url_for('main'))

@app.route("/lowCP", methods=['GET', 'POST'])
def lowCP():    #低轉換溢價清單
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        try:
            if vip_name=='shun' or vip_name=='jack':
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(
                    f"select * from {vip_name} where 轉換溢價率 < 0 and 轉換比例 < 30 ORDER BY 轉換溢價率 DESC")
                recs = cursor.fetchall()
            else:
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(
                    "select * from data where 轉換溢價率 < 0 and 轉換比例 < 30 ORDER BY 轉換溢價率 DESC")
                recs = cursor.fetchall()
            info = "=>利用可轉債與現股之間的價差 , 實施套利方法"
            conn.commit()
            conn.close()
        except:
            info = "=>顯示清單失敗"
        log.warning(info)
        flash(info)
        return redirect(url_for('main'))

@app.route("/chase", methods=['GET', 'POST'])
def chase():    #以債追股
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        try:
            if vip_name=='shun' or vip_name=='jack':
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(
                f"select * from {vip_name} where ( 轉換溢價率 not like '%無%' and 轉換溢價率 > 7 and 轉換比例 < 10) ORDER BY 轉換溢價率 DESC")
                recs = cursor.fetchall()
            else:
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(
                "select * from data where ( 轉換溢價率 not like '%無%' and 轉換溢價率 > 7 and 轉換比例 < 10) ORDER BY 轉換溢價率 DESC")
                recs = cursor.fetchall()
            conn.commit()
            conn.close()
            info = "=> 篩選轉換溢價率 > 7% 以上 , 轉換比例 < 10% 以下 ,找出有機會發動的個股 "
        except:
            info = "=>顯示清單失敗"
        log.warning(info)
        flash(info)
        return redirect(url_for('main'))

@app.route("/qryName", methods=['GET', 'POST'])
def qryName():  #搜尋功能
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            nm = request.form.get('codename')
            try:
                conn = sqlite3.connect('mydb.db')
                cursor = conn.execute(
                    f"select * from {vip_name} where 代碼 like '{nm}%' or 可轉債名稱 like '%{nm}%'")
                recs = cursor.fetchall()
                conn.commit()
                conn.close()
                info = "=>查詢成功"
                log.warning(info)
                flash(info)
            except:
                info = "=>查詢失敗"
                log.warning(info)
                flash(info)
            return redirect(url_for('main'))
        else:
            return render_template('main.html', title=appTitle , recs=recs)

@app.route("/optional", methods=['GET', 'POST'])
def optional(): #添加自選(按鈕)
    global recs
    # recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            nm = request.form['submit_button']
            try:
                if vip_name=='shun' or vip_name=='jack':
                    conn = sqlite3.connect('mydb.db')
                    cursor=conn.execute(f"select * from {vip_name} where 代碼='{nm}' ")
                    add = cursor.fetchall()
                    for record in add:
                        if  record[24] == '0':
                            conn.execute(f" update {vip_name} set 自選='1' where 代碼='{nm}'; ")
                            info = "=>加入"
                        else:
                            conn.execute(f" update {vip_name} set 自選='0' where 代碼='{nm}'; ")
                            info = "=>移除"
                        log.warning(info)
                        flash(info)
                else:
                    conn = sqlite3.connect('mydb.db')
                    cursor=conn.execute(f"select * from data where 代碼='{nm}' ")
                    add = cursor.fetchall()
                    for record in add:
                        if  record[24] == '0':
                            conn.execute(f" update data set 自選='1' where 代碼='{nm}'; ")
                            info = "=>加入"
                        else:
                            conn.execute(f" update data set 自選='0' where 代碼='{nm}'; ")
                            info = "=>移除"
                        log.warning(info)
                        flash(info)
                conn.commit()
                conn.close()
            except:
                info = "=>自選失敗"
                log.warning(info)
                flash(info)
            return redirect(url_for('main'))
        else:
            info = "=>例外失敗"
            log.warning(info)
            flash(info)
            return render_template('main.html', title=appTitle , recs=recs)

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist(): #自選清單
    global recs
    recs = []
    vip_name=session.get('username')
    if not chkSessionOK():  # 檢查 Session 是否存在
        return redirect(url_for('login'))
    else:
        try:
            if vip_name=='shun' or vip_name=='jack':
                conn = sqlite3.connect('mydb.db')
                cursor=conn.execute(f"select * from {vip_name} where 自選='1' ")
                recs = cursor.fetchall()
                info = "=>自選清單"
            else:
                conn = sqlite3.connect('mydb.db')
                cursor=conn.execute("select * from data where 自選='1' ")
                recs = cursor.fetchall()
                info = "=>自選清單"
            conn.commit()
            conn.close()
        except:
            info = "=>失敗"
        log.warning(info)
        flash(info)
        return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
    # app.run(port=5500)