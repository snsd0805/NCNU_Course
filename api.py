from flask import Flask, render_template, request
import requests
import json
import sqlite3

app = Flask(__name__)

def facebookAuth(token):
    url = "https://graph.facebook.com/v9.0/me?access_token={}"
    
    response = requests.get(url.format(token))
    data = json.loads(response.text)

    # 若 access code 通過 facebook 驗證
    if response.status_code == 200:
        return True, data['id'], data['name']
    else:
        return False, None, None

@app.route('/courseTable', methods=["POST"])
def get():
    # 若 access code 通過 facebook 驗證
    status, uid, name = facebookAuth(request.values['token'])
    
    if status:        
        # 由資料庫提取資料
        with sqlite3.connect('data.db') as conn:
            sql = "SELECT `json` FROM `courseTables` WHERE `uid`=?"

            data = conn.execute(sql, [uid]).fetchone()
            # 已經存在使用者，直接回傳 課表json
            if data:
                ansJSON = data[0]
                return json.dumps({
                    "status": "ok",
                    "data": ansJSON
                })

            # 使用者第一次使用，回傳並寫入空json
            else:
                sql = "INSERT INTO `courseTables` VALUES(NULL, ?, ?, ?)"
                conn.execute(sql, [uid, '[]', name])
                conn.commit()
                return json.dumps({
                    "status": "ok",
                    "data": "[]"
                })
        
    # access code 可能是偽造的
    else:
        return '{"status": "error access code"}', 403

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
