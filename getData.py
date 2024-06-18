import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs

session = requests.Session()

courses = []
generalCourse = []

def getDepartmentCourses():
    response = session.get('https://sis.ncnu.edu.tw/guest?school=ncnu')
    soup = bs(response.text, 'html.parser')
    token = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')
    response = session.post('https://sis.ncnu.edu.tw/b09/b09120', data={
        '_token': token,
        'srh[ACADYear][]': '113',
        'srh[Semester][]': '1',
        'srh[DayfgID][]': '',
        'srh[ClassTypeID][]': '',
        'srh[CollegeID][]': '',
        'srh[UnitID][]': '',
        'srh[StudyCourseCategoryNo]': '',
        'srh[ClassID]': '',
        'srh[SemesterCourseNo]': '',
        'srh[Teacher]': '',
        'srh[SemesterCourseName]': '',
        'srh[TeaLanguage][]': '',
        'srh[ClassRoomType][]': '',
        'srh[ClassRoom][]': '',
        'srh[DayKind][]': '',
        'srh[SectionBeg][]': '',
        'srh[SectionEnd][]': '',
        'srh[IsFollowUp][]': '',
        'tb_length': '10',
        'tb_sel': '',
        'tb_cancel': '',
        'event': 'search'
    })
    
    data_line = ''
    for line in response.text.splitlines():
        if 'setDataTables' in line:
            data_line = line
            break

    data_line = '{'.join(data_line.split('{')[1:])
    data_line = '}'.join(data_line.split('}')[:-1])
    data_line = '{' + data_line + '}'

    data = json.loads(data_line)

    with open('new.json', 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)
    print(data.keys())

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
            # if count == 0 and len(line) != 2:
            #     print("{} 可能輸入錯誤 - {}".format(line[0], department))
            line = fp.readline()

    print("還沒有對應到的課程：")
    for course in courses:
        if course['department'] == "99, 通識":
            course['department'] = "99, 通識（未分類）"
            print("{} {}".format(course['number'], course['name']))

    with open("歷年課程資料/{}_output.json".format(YEAR), "w") as fp:
        json.dump(courses, fp, ensure_ascii=False)


if __name__ == "__main__":
    getDepartmentCourses()
