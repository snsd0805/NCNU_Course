import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs

session = requests.Session()

mainURL = "https://ccweb.ncnu.edu.tw/student/"
courses = []
generalCourse = []

def login(username, password):
    global session
    response = session.get('https://ccweb.ncnu.edu.tw/student/login.php')
    root = bs(response.text, 'html.parser')
    loginToken = root.find('input', {'name': 'token'}).get('value')

    # request login page
    response = session.post(
        "https://ccweb.ncnu.edu.tw/student/login.php",
        data={
            'token': loginToken,
            'modal': '0',
            'username': username,
            'password': password,
            'type': 'a'
        }
    )

    # 成功的話 return http 302, redirect
    if len(response.history)!=0:
        return True
    else:
        return False

def curlDepartmentCourseTable(year):
    '''
        先取得各科系的開課表格連結
        再將連結丟給 extractDepartmentCourseTable() 取得課程資訊
    '''
    print("取得所有課程資料：")

    # 切換年度，應該是用 cookie 儲存當前閱覽的年份
    url = 'https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?cmd=search&t=aspmaker_course_opened_detail_view&z_year=%3D&x_year={}&z_courseid=%3D&x_courseid=&z_cname=LIKE&x_cname=&z_deptid=%3D&x_deptid=&z_division=LIKE&x_division=&z_grade=%3D&x_grade=&z_teachers=LIKE&x_teachers=&z_not_accessible=LIKE&x_not_accessible='
    response = session.get(url.format(year))

    # 取得 所有課程的 csv
    response = session.get('https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?export=csv')
    with open("allCourses.csv", "wb") as fp:
        fp.write(response.content)

def extractDepartmentCourseTable(year):
    '''
        透過各科系連結取得課程資訊
        若為通識類別還要跟csv檔資料做對應，取得正確通識類別
        
        對應後存取到 output.json
    '''
    with open("allCourses.csv") as fp:
        csvData = fp.read()

    ans = []
    courses = csvData.split('"\n')[1:-1]
    for course in courses:
        course = course.replace('\n', '.')
        # print(course)
        data = course[1:].split('","')
        
        courseObj = {}

        baseLink = "https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewview.php?showdetail=&year={}&courseid={}&_class={}&modal=2"
        courseObj['link']        = baseLink.format(year, data[1].zfill(6), data[2])
        courseObj['year']        = data[0]
        courseObj['number']      = data[1]
        courseObj['class']       = data[2]
        courseObj['name']        = data[3]
        courseObj['department']  = data[4]
        courseObj['graduated']   = data[6]
        courseObj['grade']       = data[7]
        courseObj['teacher']     = data[8]
        courseObj['place']       = data[9]
        courseObj['time']        = data[13]
        courseObj['credit']      = data[14]

        ans.append(courseObj)

    with open("歷年課程資料/{}_output.json".format(year), 'w') as fp:
        json.dump(ans, fp, ensure_ascii=False)

if __name__ == "__main__":
    year = input("年份: ")

    while True:
        username = input("學號： ")
        password = input("密碼： ")
        if login(username, password):
            break
        else:
            print("登入失敗！")
    
    curlDepartmentCourseTable(year)
    extractDepartmentCourseTable("1101")
