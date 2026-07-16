import re
import time
import requests
from bs4 import BeautifulSoup as bs

BASE = 'https://ccweb6.ncnu.edu.tw/student/'
LIST_PAGE = 'ncnu_coremin_schoolrequire_detail_viewlist.php'

# 用來查詢的「入學年度」區間。課號本身跟查詢時填的入學年度無關（同一個課號在不同
# 入學年度的查詢下都可能出現），但不同入學年度適用的核心課程規定不同，所以要合併
# 多個入學年度的查詢結果，才能拿到跟現有 generalCourse.in 對得起來的完整課號清單。
YEARS = ['115','114','113','112','111']

OUTPUT_FILE = 'general_course_lookup/generalCourse.in'

session = requests.Session()


REQUEST_TIMEOUT = 15  # 秒；避免學校伺服器不回應時整支程式卡死


def getToken():
    response = session.get(BASE + LIST_PAGE, timeout=REQUEST_TIMEOUT)
    match = re.search(r'ANTIFORGERY_TOKEN:\s*"([^"]+)"', response.text)
    return match.group(1)


def getCategories(year):
    print(year, flush=True)
    '''取得「核心類別」欄位目前所有選項，例如 "J 社會-社經與管理(105始)"'''
    token = getToken()
    response = session.post(BASE + 'api/index.php?action=lookup', data={
        'page': 'ncnu_coremin_schoolrequire_detail_view_list',
        'field': '核心類別',
        'ajax': 'updateoption',
        'language': 'zh-tw',
        'name': 'x__68385FC3985E5225',
        'v1': year,
        'token': token,
    }, headers={'X-Requested-With': 'XMLHttpRequest'}, timeout=REQUEST_TIMEOUT)

    categories = [record['0'] for record in response.json()['records']]
    print(response, flush=True)
    # 「共同選修」「共同必修」不是通識次領域，只留下有「主領域-次領域」結構的類別
    return [c for c in categories if '-' in c]


def normalizeDepartmentName(category):
    '''把 "J 社會-社經與管理(105始)" 轉成 generalCourse.in 慣用的 "社會—社經與管理" 格式'''
    name = category.split(' ', 1)[1]
    name = re.sub(r'\(?\d+始\)?$', '', name)
    return name.replace('-', '—')


def getCourseNumbers(year, category):
    print(year, category, flush=True)
    '''取得指定入學年度、指定核心類別下的所有課號'''
    params = {
        'cmd': 'search',
        't': 'ncnu_coremin_schoolrequire_detail_view',
        'z__51655B785E74': '=',
        'x__51655B785E74': year,
        'z__68385FC3985E5225': '=',
        'x__68385FC3985E5225': category,  # requests 的 params= 會自動做 URL 編碼，這裡不能再手動 quote 一次
        'recperpage': '9999',  # 一次拿完，不用翻頁
    }
    response = session.get(BASE + LIST_PAGE, params=params, timeout=REQUEST_TIMEOUT)
    soup = bs(response.text, 'html.parser')
    rows = soup.select('tr[data-rowindex]')
    print(response, len(rows), flush=True)
    return [row.find_all('td')[3].get_text(strip=True) for row in rows]


def main():
    categories = getCategories(YEARS[-1])
    print(f"共 {len(categories)} 個通識次領域類別")
    print(categories)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as fp:
        for category in categories:
            departmentName = normalizeDepartmentName(category)
            print(f"抓取 {departmentName} ({category})")

            numbers = set()
            for year in YEARS:
                numbers.update(getCourseNumbers(year, category))
                time.sleep(0.2)

            print(f"  共 {len(numbers)} 筆課號")

            fp.write(f"department {departmentName}\n")
            for number in sorted(numbers):
                fp.write(f"{number}\n")


if __name__ == "__main__":
    main()
