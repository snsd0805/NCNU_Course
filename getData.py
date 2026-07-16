import requests
import json
import os
import csv
from bs4 import BeautifulSoup as bs
import re

SEMESTER = '1132'

session = requests.Session()

courses = []
generalCourse = []

def getDepartmentCourses():
    def getCourseTime(course):
        week_map = dict(zip(['一', '二', '三', '四', '五', '六', '日'], range(1, 8)))
        # try:
        time_str = course['SemCourseTime']
        print(time_str)
        # ans = str(week_map[int(time_str[0])])
        ptr = 2
        while time_str[ptr] != ')':
            if time_str[ptr] != ',':
                ans += time_str[ptr]
            ptr += 1
        return ans
        # except:
        #    return '另訂'


    response = session.get('https://sis.ncnu.edu.tw/')
    soup = bs(response.text, 'html.parser')
    token = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')
    print(f"CSRF TOKEN: {token}")

    response = session.post('https://sis.ncnu.edu.tw/guest', data={'_token': token})
    soup = bs(response.text, 'html.parser')
    token = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')
    print(f"CSRF TOKEN: {token}")

    response = session.post('https://sis.ncnu.edu.tw/b09/b09120', data={
        '_token': token,
        'srh[ACADYear][]': SEMESTER[:3],
        'srh[Semester][]': SEMESTER[-1],
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
    soup = bs(response.text, 'html.parser')
    token = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')

    # 搜尋結果實際上是由頁面載入後另外發出的 DataTables AJAX 請求取得，
    # 上面的 srh[...] 查詢只是先把篩選條件存進 session，這邊要照 DataTables
    # 的 server-side protocol 再送一次才拿得到真正的課程資料
    columns = [
        '', 'CourseNo', 'StudyClassName', 'SemesterCourseName', 'SemesterCourseENGName',
        'CourseClassName', 'Credit', 'UnitName', 'DayfgClassTypeName', 'Grade', 'Teacher',
        'SemCourseTime', 'ClassRoom', 'Memo', 'TeaLanguage', 'StdAmtLow', 'StdAmtUp',
        'VolCnt', 'VolGetCnt', 'SelAmt', 'SemesterCourseNo', 'Choose'
    ]

    def buildDataTablesPayload(length):
        payload = {
            'draw': '1',
            'start': '0',
            'length': str(length),
            'search[value]': '',
            'search[regex]': 'false',
        }
        for i, name in enumerate(columns):
            payload[f'columns[{i}][data]'] = name
            payload[f'columns[{i}][name]'] = ''
            payload[f'columns[{i}][searchable]'] = 'true'
            payload[f'columns[{i}][orderable]'] = 'true'
            payload[f'columns[{i}][search][value]'] = ''
            payload[f'columns[{i}][search][regex]'] = 'false'
        return payload

    ajaxHeaders = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-TOKEN': token,
    }

    # 先探詢總筆數，再用剛好的 length 一次拿完全部資料
    probe = session.post('https://sis.ncnu.edu.tw/b09/b09120', data=buildDataTablesPayload(1), headers=ajaxHeaders).json()
    total = int(probe['recordsTotal'])
    print(f"共 {total} 筆課程")

    result = session.post('https://sis.ncnu.edu.tw/b09/b09120', data=buildDataTablesPayload(total), headers=ajaxHeaders).json()

    courses = []
    for course in result['data']:
        courses.append({
            'link': f'https://sis.ncnu.edu.tw/b09/b09120/view/{course["SemesterCourseID"]}',
            'year': SEMESTER,
            'number': course['SemesterCourseID'],   # course['SemesterCourseNo']
            'class': course['StudyClassName'],
            'name': re.search('>.*<', course['SemesterCourseName']).group(0)[1:-1] \
                        if '<a href' in course['SemesterCourseName'] else course['SemesterCourseName'],
            'department': course['UnitName'],
            'graduated': course['DayfgClassTypeName'],
            'grade': '0',
            'teacher': course['Teacher'],
            'place': course['ClassRoom'] if course['ClassRoom'] else '另訂',
            'time': course['SemCourseTime'].replace(',','').replace(' ', '') if course['SemCourseTime'] else '另訂',# getCourseTime(course),
            'credit': course['Credit'],
            'max': course['StdAmtUp'],
            'memo': course['Memo'] or '',
        })
        '''
        'semester_course_number': course['SemesterCourseNo'],
        'english_name': course['SemesterCourseENGName'],
        'choose': course['Choose'],
        'course_class_name': course['CourseClassName'],
        '''

    # 通識領域
    fields = [
        '法政與教育次領域', '國際連結(東南亞)次領域', '工程與科技次領域', '文學與藝術次領域', '歷史哲學與文化次領域', \
        '生命與科學次領域', '社會創新(在地實踐)次領域', '社經與管理次領域', '淨零永續(綠概念)次領域'
    ]
    for course in courses:
        if course['department'] == '通識領域課程':
            course['memo'] = course['memo'].replace(',', '，')
            if course['memo'] != '':
                field = ''
                for f in fields:
                    if f in course['memo']:
                        field = f

                if field:
                    course['department'] = f"※ 通識－{field}"
                    if '，' in course['memo']: 
                        field, limit = course['memo'].split('，')
                        course['name'] += f'({limit})' 
                else:
                    course['department'] = f"※ 通識－學校未正常分類之課程"
            else:
                course['department'] = f"※ 通識－學校未正常分類之課程"

    for course in courses:
        print(course['name'])

    with open(f'歷年課程資料/{SEMESTER}_output.json', 'w', encoding='utf-8') as fp:
        json.dump(courses, fp, ensure_ascii=False)

if __name__ == "__main__":
    getDepartmentCourses()
