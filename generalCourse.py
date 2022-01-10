import json

with open("output.json") as fp:
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

with open("output.json", "w") as fp:
    json.dump(courses, fp, ensure_ascii=False)

