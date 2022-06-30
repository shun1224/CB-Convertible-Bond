import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

def createDB(): # 建立資料庫
    try:
        conn = sqlite3.connect('mydb.db')
        conn.execute(f'''
            create table  if not exists data
            (
                iid  integer primary key autoincrement,
                可轉債名稱   char(10)               not null,
                轉換標的名稱   char(10)             not null,
                上市櫃別    char(10)             not null,
                擔保銀行   char(20)             not null,
                最新CB收盤價    varchar(30)             not null,
                轉換價值     char(10)             not null,
                CBAS權利金    char(20)             not null,
                轉換溢價率    varchar(30)            not null,
                最新股票收盤價    char(10)             not null,
                目前轉換價    char(10)             not null,
                發行時轉換價    char(10)             not null,
                發行價格    char(10)             not null,
                發行總額    char(10)             not null,
                最新餘額     char(10)             not null,
                轉換比例    varchar(30)             not null,
                發行日     char(10)             not null,
                到期日    char(10)             not null,
                到期賣回價格     char(10)             not null,
                下次提前賣回日    char(10)             not null,
                下次提前賣回價格    char(10)             not null,
                詳細發行辦法    char(10)             not null,
                財務數據        char(10)             not null,
                代碼        char(10)               not null,
                自選        char(10)               not null
            );
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print('發生錯誤...')
        print(f'錯誤訊息為{e}')

def vipDB(vip_name): # 建立資料庫
    try:
        conn = sqlite3.connect('mydb.db')
        conn.execute(f'''
            create table  if not exists {vip_name}
            (
                iid  integer primary key autoincrement,
                可轉債名稱   char(10)               not null,
                轉換標的名稱   char(10)             not null,
                上市櫃別    char(10)             not null,
                擔保銀行   char(20)             not null,
                最新CB收盤價    varchar(30)             not null,
                轉換價值     char(10)             not null,
                CBAS權利金    char(20)             not null,
                轉換溢價率    varchar(30)            not null,
                最新股票收盤價    char(10)             not null,
                目前轉換價    char(10)             not null,
                發行時轉換價    char(10)             not null,
                發行價格    char(10)             not null,
                發行總額    char(10)             not null,
                最新餘額     char(10)             not null,
                轉換比例    varchar(30)             not null,
                發行日     char(10)             not null,
                到期日    char(10)             not null,
                到期賣回價格     char(10)             not null,
                下次提前賣回日    char(10)             not null,
                下次提前賣回價格    char(10)             not null,
                詳細發行辦法    char(10)             not null,
                財務數據        char(10)             not null,
                代碼        char(10)               not null,
                自選        char(10)               not null
            );
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print('發生錯誤...')
        print(f'錯誤訊息為{e}')

def importData(j,k,vip_name):   #匯入資料表
    o=[]
    t=[]
    data=[]
    totle=1
    se=0
    try:
        conn = sqlite3.connect('mydb.db')
        for one in j:
            o.append(one) if totle % 2 else t.append(one)
            totle+=1
            # print(type(one),one)
            if one == '財報狗, goodinfo':
                o.append("代碼")
                t.append(k[se])
                dict_from_list = zip(o, t)
                data.append(dict(dict_from_list))
                o=[]
                t=[]
                se+=1
        if vip_name=='shun' or vip_name=='jack':
            for i in data:
                key_list = list(i.keys())
                conn.execute(f"insert into {vip_name} (可轉債名稱, 轉換標的名稱, 上市櫃別, 擔保銀行, 最新CB收盤價, 轉換價值, CBAS權利金, 轉換溢價率, 最新股票收盤價, 目前轉換價,\
                    發行時轉換價, 發行價格, 發行總額, 最新餘額, 轉換比例, 發行日, 到期日, 到期賣回價格, 下次提前賣回日, 下次提前賣回價格, 詳細發行辦法, 財務數據, 代碼, 自選) \
                        select '{i[key_list[0]]}', '{i[key_list[1]]}', '{i[key_list[2]]}','{i[key_list[3]]}', '{i[key_list[4]]}', '{i[key_list[5]]}','{i[key_list[6]]}', '{i[key_list[7]]}', \
                            '{i[key_list[8]]}','{i[key_list[9]]}', '{i[key_list[10]]}', '{i[key_list[11]]}','{i[key_list[12]]}', '{i[key_list[13]]}', '{i[key_list[14]]}','{i[key_list[15]]}', \
                            '{i[key_list[16]]}', '{i[key_list[17]]}','{i[key_list[18]]}', '{i[key_list[19]]}', '{i[key_list[20]]}','{i[key_list[21]]}','{i[key_list[22]]}','0' \
                        where not exists(select 1 from {vip_name} where 可轉債名稱='{i[key_list[0]]}'and 轉換標的名稱='{i[key_list[1]]}'and 上市櫃別='{i[key_list[2]]}'and 擔保銀行='{i[key_list[3]]}'and \
                            最新CB收盤價='{i[key_list[4]]}'and 轉換價值='{i[key_list[5]]}'and CBAS權利金='{i[key_list[6]]}'and 轉換溢價率='{i[key_list[7]]}'and 最新股票收盤價='{i[key_list[8]]}'and \
                            目前轉換價='{i[key_list[9]]}'and 發行時轉換價='{i[key_list[10]]}'and 發行價格='{i[key_list[11]]}'and 發行總額='{i[key_list[12]]}'and 最新餘額='{i[key_list[13]]}'and \
                            轉換比例='{i[key_list[14]]}'and 發行日='{i[key_list[15]]}'and 到期日='{i[key_list[16]]}'and 到期賣回價格='{i[key_list[17]]}'and 下次提前賣回日='{i[key_list[18]]}'and \
                            下次提前賣回價格='{i[key_list[19]]}'and 詳細發行辦法='{i[key_list[20]]}'and 財務數據='{i[key_list[21]]}' and 代碼='{i[key_list[22]]}');")
        else:
            for i in data:
                key_list = list(i.keys())
                conn.execute(f"insert into data (可轉債名稱, 轉換標的名稱, 上市櫃別, 擔保銀行, 最新CB收盤價, 轉換價值, CBAS權利金, 轉換溢價率, 最新股票收盤價, 目前轉換價,\
                    發行時轉換價, 發行價格, 發行總額, 最新餘額, 轉換比例, 發行日, 到期日, 到期賣回價格, 下次提前賣回日, 下次提前賣回價格, 詳細發行辦法, 財務數據, 代碼, 自選) \
                        select '{i[key_list[0]]}', '{i[key_list[1]]}', '{i[key_list[2]]}','{i[key_list[3]]}', '{i[key_list[4]]}', '{i[key_list[5]]}','{i[key_list[6]]}', '{i[key_list[7]]}', \
                            '{i[key_list[8]]}','{i[key_list[9]]}', '{i[key_list[10]]}', '{i[key_list[11]]}','{i[key_list[12]]}', '{i[key_list[13]]}', '{i[key_list[14]]}','{i[key_list[15]]}', \
                            '{i[key_list[16]]}', '{i[key_list[17]]}','{i[key_list[18]]}', '{i[key_list[19]]}', '{i[key_list[20]]}','{i[key_list[21]]}','{i[key_list[22]]}','0' \
                        where not exists(select 1 from data where 可轉債名稱='{i[key_list[0]]}'and 轉換標的名稱='{i[key_list[1]]}'and 上市櫃別='{i[key_list[2]]}'and 擔保銀行='{i[key_list[3]]}'and \
                            最新CB收盤價='{i[key_list[4]]}'and 轉換價值='{i[key_list[5]]}'and CBAS權利金='{i[key_list[6]]}'and 轉換溢價率='{i[key_list[7]]}'and 最新股票收盤價='{i[key_list[8]]}'and \
                            目前轉換價='{i[key_list[9]]}'and 發行時轉換價='{i[key_list[10]]}'and 發行價格='{i[key_list[11]]}'and 發行總額='{i[key_list[12]]}'and 最新餘額='{i[key_list[13]]}'and \
                            轉換比例='{i[key_list[14]]}'and 發行日='{i[key_list[15]]}'and 到期日='{i[key_list[16]]}'and 到期賣回價格='{i[key_list[17]]}'and 下次提前賣回日='{i[key_list[18]]}'and \
                            下次提前賣回價格='{i[key_list[19]]}'and 詳細發行辦法='{i[key_list[20]]}'and 財務數據='{i[key_list[21]]}' and 代碼='{i[key_list[22]]}');")
        conn.commit()
        conn.close()
    except FileNotFoundError:
        print('找不到檔案...')
    except Exception as e:
        print('開檔發生錯誤...')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        print(f'錯誤檔案為：{e.filename}')

def r1(vip_name): #爬蟲
    k=[]
    j=[]
    #防止彈出視窗
    options = Options()
    options.add_argument("--disable-notifications")
    URL = "https://thefew.tw/cb"
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(URL)

    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/nav/div[2]/div/div[2]/a'))
    )
    login.click()
    login1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/a'))
    )
    login1.click()

    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    )
    email.send_keys('9a717017@gm.student.ncut.edu.tw')
    login2 = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span')
    login2.click()

    time.sleep(2)
    password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    password.send_keys('s25265289')
    login3 = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/span')
    login3.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'cb-table'))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    simps = soup.find_all("div",class_='w-1/3')
    for simp in simps:
        k.append(simp.text.replace("\n",""))
    films = soup.find_all("td",class_='w-1/2')
    for film in films:
        j.append(film.text.replace("\n",""))

    if os.path.isfile('mydb.db') == False:
        createDB()
    importData(j,k,vip_name)
