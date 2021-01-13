import requests
import json
import os
from bs4 import BeautifulSoup as bs


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Cookie': '輸入登入暨大教務系統後所得到的cookie'
}

mainURL = "https://ccweb.ncnu.edu.tw/student/"
courses = []

def curlDepartmentCourseTable(year):
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

# def curlGeneralCoursePage():    
#     print("取得通識課資料：")
#     progress = tqdm(total=generalFinalPage)
#     for page in range(1, generalFinalPage+1):
#         url = 'https://ccweb.ncnu.edu.tw/student/aspmaker_student_common_rank_courses_viewlist.php?pageno={}'.format(page)
#         response = requests.get(url, headers=header)
#         data = response.text
#         with open('general/{}.html'.format(page), 'w') as fp:
#             fp.write(data)
#         progress.update(1)

def extractDepartmentCourseTable(departmentName, link):
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
        courses.append(courseObj)
    
    with open('output.json', 'w') as fp:
        json.dump(courses, fp)

    

    # print("解析所有課程html：")
    # progress = tqdm(total=allFinalPage)
    # for pageNumber in range(1, allFinalPage+1):
    #     html = ""
    #     with open('all/{}.html'.format(pageNumber), 'r') as fp:
    #         html = fp.read()
    #     root = bs(html, "html.parser")
    #     courses = root.find_all('tr')
    #     courses = courses[1:]
    #     for course in courses:
    #         courseObj = {}
    #         tds = course.find_all('td')
    #         tds = tds[1:]
    #         courseObj['year'] = tds[0].text.replace('\n', '')
    #         courseObj['number'] = tds[1].text.replace('\n', '')
    #         courseObj['name'] = tds[3].text.replace('\n', '')
    #         courseObj['class'] = tds[2].text.replace('\n', '')
    #         courseObj['department'] = tds[4].text.replace('\n', '')
    #         courseObj['graduated'] = tds[5].text.replace('\n', '')
    #         courseObj['grade'] = tds[6].text.replace('\n', '')
    #         courseObj['teacher'] = tds[7].text.replace('\n', '')
    #         courseObj['place'] = tds[8].text.replace('\n', '')
    #         courseObj['time'] = tds[10].text.replace('\n', '')

    #         courseObjList[
    #             tds[1].text.replace('\n', '')
    #             +
    #             tds[2].text.replace('\n', '')
    #         ] = courseObj
    #     progress.update(1)

# def extractGeneralCourse():
#     print("解析通識課html：")
#     progress = tqdm(total=generalFinalPage)
#     for pageNumber in range(1, generalFinalPage+1):
#         html = ""
#         with open('general/{}.html'.format(pageNumber), 'r') as fp:
#             html = fp.read()
#         root = bs(html, "html.parser")
#         courses = root.find_all('tr')
#         courses = courses[1:]
#         for course in courses:
#             courseObj = {}
#             tds = course.find_all('td')
#             number = tds[3].text.replace('\n', '')
#             classNum = tds[4].text.replace('\n','')
#             major = tds[1].text.replace('\n', '')
#             name = tds[6].text.replace('\n', '')
#             old = courseObjList[number+classNum]['department']
#             if old != "90, 體育室":
#                 courseObjList[number+classNum]['department'] = major
#         progress.update(1)



year = input("年份: ")
curlDepartmentCourseTable(year)
# extractAllCourse()
# curlGeneralCoursePage()
# extractGeneralCourse()

# out = []
# count = 0
# for item in courseObjList:
#     count = count+1
#     out.append(courseObjList[item])

# with open('output.json', 'w') as fp:
#     fp.write(json.dumps(out, ensure_ascii=False))
# print(count)
