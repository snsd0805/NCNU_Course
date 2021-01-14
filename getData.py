import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Cookie': '輸入登入暨大教務系統後所得到的cookie'
}

mainURL = "https://ccweb.ncnu.edu.tw/student/"
courses = []
generalCourse = []

def getGeneralCourseData(year):
    '''
        透過年份取得 通識課程分類的csv檔
        供後續課程對應。
        
        先儲存到 generalCourse list，後續再用 courseID 對應通識分類
    '''

    # 教務系統有開放 年度的query
    # 但實際操作後似乎僅開放當前學年度
    response = requests.get(mainURL+"aspmaker_student_common_rank_courses_viewlist.php?x_studentid=0&z_studentid=LIKE&x_year={}&z_year=%3D&cmd=search&export=csv".format(year), headers=header)
    data = response.text

    courses = data.split('\r\n')[1:-1]
    for course in courses:
        course = course.split(',')
        generalCourse.append(course)

def curlDepartmentCourseTable(year):
    '''
        先取得各科系的開課表格連結
        再將連結丟給 extractDepartmentCourseTable() 取得課程資訊
    '''
    print("取得所有課程資料：")

    response = requests.get(mainURL+"aspmaker_course_opened_semester_stat_viewlist.php?x_year={}&recperpage=ALL".format(year), headers=header)
    data = response.text
    root = bs(data, "html.parser")
    
    count = 1
    departmentsTR = root.findAll('tr')[1:]  # 清除 thead
    for tr in departmentsTR:
        name = tr.findAll('td')[4].find('span').find('span').string # 取得 科系名稱
        link = mainURL + tr.find('a').get('data-url').replace('amp;', '')     # 清除不必要符號， 取得 連結
        print("擷取{}課程... ({}/{})...".format(name, count, len(departmentsTR)))
        count += 1
        extractDepartmentCourseTable(name, link)    # 透過連結 開始擷取 各科系課程

def extractDepartmentCourseTable(departmentName, link):
    '''
        透過各科系連結取得課程資訊
        若為通識類別還要跟csv檔資料做對應，取得正確通識類別
        
        對應後存取到 output.json
    '''
    response = requests.get(link, headers=header)
    data = response.text
    root = bs(data, "html.parser")

    courseTR = root.findAll('tr')[1:] # 清除 thead
    for tr in courseTR:
        courseObj = {}
        tds = tr.find_all('td')

        courseObj['link'] = mainURL + tds[0].find('a').get('href')
        courseObj['year'] = tds[1].find('span').string
        courseObj['number'] = tds[2].find('span').string
        courseObj['class'] = tds[3].find('span').string
        courseObj['name'] = tds[4].find('span').string
        courseObj['department'] = tds[5].find('span').string
        courseObj['graduated'] = tds[6].find('span').string
        courseObj['grade'] = tds[7].find('span').string
        courseObj['teacher'] = tds[8].find('span').string
        courseObj['place'] = tds[9].find('span').string
        courseObj['time'] = tds[11].find('span').string

        if courseObj['department']=="99, 通識" :
            flag = False
            for row in generalCourse:
                if row[2] == '"{}"'.format(courseObj['number']):
                    courseObj['department'] = row[0].replace('"', '')
                    generalCourse.remove(row)
                    flag = True
                    break
            if not flag:
                print(" - 找不到對應的通識類別： {} ( {} )".format(courseObj['name'], courseObj['number']))
        
        courses.append(courseObj)
    
    with open('output.json', 'w') as fp:
        json.dump(courses, fp)


if __name__ == "__main__":
    year = input("年份: ")

    getGeneralCourseData(year)
    curlDepartmentCourseTable(year)

    print("\n\n=====================")
    print("未列入追蹤的通識課程")
    print("=====================\n")

    for notIn in generalCourse:
        if "體育:" not in notIn[5]:
            print(" - 未列入追蹤的新通識課程： {}".format(notIn))