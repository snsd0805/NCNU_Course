import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs
import re

SEMESTER = '1131'

session = requests.Session()

courses = []
generalCourse = []

def getDepartmentCourses():
    def getCourseTime(course):
        week_map = dict(zip(['一', '二', '三', '四', '五', '六', '日'], range(1, 8)))

        try:
            time_str = course['SemCourseTime']
            ans = str(week_map[time_str[0]])
            ptr = 2
            while time_str[ptr] != ')':
                if time_str[ptr] != ',':
                    ans += time_str[ptr]
                ptr += 1
            return ans
        except:
            return '另訂'

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

    courses = []
    for course in data['data']:
        courses.append({
            'link': f'https://sis.ncnu.edu.tw/b09/b09120/view/{course["SemesterCourseID"]}',
            'year': SEMESTER,
            'number': course['SemesterCourseID'],   # course['SemesterCourseNo']
            'class': course['StudyClassName'],
            'name': re.search('>.*<', course['SemesterCourseName']).group(0)[1:-1] \
                        if '<a href' in course['SemesterCourseName'] else course['SemesterCourseName'],
            'department': course['StudyCourseCategoryNames'],
            'graduated': course['DayfgClassTypeName'],
            'grade': '0',
            'teacher': course['Teacher'],
            'place': course['ClassRoom'] if course['ClassRoom'] != '' else '另訂',
            'time': getCourseTime(course),
            'credit': course['Credit'],
            'max': course['StdAmtUp'],
            'memo': course['Memo'],
        })
        '''
        'semester_course_number': course['SemesterCourseNo'],
        'english_name': course['SemesterCourseENGName'],
        'choose': course['Choose'],
        'course_class_name': course['CourseClassName'],
        '''

    # 通識領域
    for course in courses:
        if course['department'] == '通識領域課程':
            if course['memo'] != '':
                if '，' in course['memo']: 
                    field, limit = course['memo'].split('，')
                    course['department'] = field
                    course['name'] += f'({limit})' 
                else:
                    course['department'] = course['memo']
            else:
                course['department'] += '(無分類)'

    with open(f'歷年課程資料/{SEMESTER}_output.json', 'w') as fp:
        json.dump(courses, fp, ensure_ascii=False)


def updateGeneralCourse():
    with open("歷年課程資料/{}_output.json".format(SEMESTER)) as fp:
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
