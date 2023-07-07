from flask import Flask, render_template, request
import requests
import json
import sqlite3
from flask_cors import  CORS

app = Flask(__name__)
CORS(app, resources={r"/.*": {"origins": ["https://course.snsd0805.com"]}})

@app.route('/courseTable', methods=["GET"])
def get():
    uid = request.values['uid']
    name = request.values['name']
    
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
        

@app.route('/courseTable', methods=["POST"])
def save():
    # 先驗證 access code 是否正確
    jsonData = request.get_json()
    uid = jsonData['uid']
    data = jsonData['data']

    with sqlite3.connect('data.db') as conn:
        sql = "UPDATE `courseTables` SET `json`=? WHERE `uid`=?"
        conn.execute(sql, [json.dumps(data, ensure_ascii=False), uid])
        conn.commit()
        return '{"status": "saved"}', 200

@app.route('/shared/<uid>', methods=['GET'])
def shared(uid):
    with sqlite3.connect('data.db') as conn:
        sql = "SELECT `json` FROM `courseTables` WHERE `uid`=?"

        data = conn.execute(sql, [uid]).fetchone()

        if data:
            ansJSON = data[0]
            return json.dumps({
                "status": "ok",
                "data": ansJSON
            }), 200
        else:
            return json.dumps({
                "status": "not found",
            }), 404

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
