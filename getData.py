import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs

USERNAME = ""
PASSWORD = ""
YEAR = 1122

session = requests.Session()

mainURL = "https://ccweb6.ncnu.edu.tw/student/"
courses = []
generalCourse = []

def login(username, password):
    global session
    response = session.get('https://ccweb6.ncnu.edu.tw/student/login.php')
    print(response.text)
    root = bs(response.text, 'html.parser')
    loginToken = root.find('input', {'name': 'token'}).get('value')

    # request login page
    response = session.post(
        "https://ccweb6.ncnu.edu.tw/student/login.php",
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
    url = 'https://ccweb6.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?cmd=search&t=aspmaker_course_opened_detail_view&z_year=%3D&x_year={}&z_courseid=%3D&x_courseid=&z_cname=LIKE&x_cname=&z_deptid=%3D&x_deptid=&z_division=LIKE&x_division=&z_grade=%3D&x_grade=&z_teachers=LIKE&x_teachers=&z_not_accessible=LIKE&x_not_accessible='
    response = session.get(url.format(year))

    # 取得 所有課程的 csv
    response = session.get('https://ccweb6.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?export=csv')
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

        baseLink = "https://ccweb6.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?cmd=search&t=aspmaker_course_opened_detail_view&z_year=%3D&x_year={}&x_courseid={}"
        courseObj['link']        = baseLink.format(year, data[1].zfill(6))
        courseObj['year']        = data[0]
        courseObj['number']      = data[1]
        courseObj['class']       = data[2]
        courseObj['name']        = data[3]
        courseObj['department']  = data[4]
        courseObj['graduated']   = data[6]
        courseObj['grade']       = data[7]
        courseObj['teacher']     = data[8]
        courseObj['place']       = data[9]
        courseObj['time']        = data[13].replace(' ', '')
        courseObj['credit']      = data[14]

        ans.append(courseObj)

    with open("歷年課程資料/{}_output.json".format(year), 'w') as fp:
        json.dump(ans, fp, ensure_ascii=False)

def updateGeneralCourse():
    with open("歷年課程資料/{}_output.json".format(YEAR)) as fp:
        courses = json.load(fp)

    with open("generalCourse.in") as fp:
        line = fp.readline()
        while line:
            count = 0
            line = line.split()
            if len(line) == 2:
                department = line[1]
            else:
                for course in courses:
                    if course['number'] == line[0]:
                        course['department'] = department
                        count += 1
            if count == 0 and len(line) != 2:
                print("{} 可能輸入錯誤 - {}".format(line[0], department))
            line = fp.readline()

    print("還沒有對應到的課程：")
    for course in courses:
        if course['department'] == "99, 通識":
            course['department'] = "99, 通識（未分類）"
            print("{} {}".format(course['number'], course['name']))

    with open("歷年課程資料/{}_output.json".format(YEAR), "w") as fp:
        json.dump(courses, fp, ensure_ascii=False)



if __name__ == "__main__":
    while True:
        username = USERNAME
        password = PASSWORD
        if login(username, password):
            print("登入成功！")
            break
        else:
            print("登入失敗！")
    
    curlDepartmentCourseTable(YEAR)
    extractDepartmentCourseTable(YEAR)
    updateGeneralCourse()
