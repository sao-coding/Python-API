import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from PIL import Image, ImageDraw, ImageFont
import datetime
import pathlib
import os
import requests
from datetime import datetime


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "Hello World test!"

@app.route('/api', methods=['GET'])
def api():

    date = []
    count = []

    f = open('/volume1/music/form.diff', 'r' , encoding='utf-8')
    for line in f.readlines():
        data = line.split("|")
        if data[0] not in date:
            if "#" not in data[0]:
                date.append(data[0])
            else:
                if "來亂的人" in date:
                    continue
                else:
                    date.append("來亂的人")
    f.close()
    date.pop(0)
    date.sort()
    count = [0]*len(date)

    f = open('/volume1/music/form.diff', 'r' , encoding='utf-8')
    for line in f.readlines():
        data = line.split("|")
        if "日期" not in data[0]:
            if "#" in data[0]:
                key = date.index("來亂的人")
                count[key] += 1
            else:
                key = date.index(data[0])
                count[key] += 1
    api = dict(zip(date,count))
    api = {"jsonarray":[api]}
    return jsonify(api)

@app.route('/rank', methods=['GET'])
def rank():
    db = pymysql.connect(host='localhost', port=3306, user='ian1234280', passwd='User.-.0987', db='Dodge', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM data"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    # api = dict(zip(date,count))
    # api = {"jsonarray":[api]}
    # print(type(data))
    # data = map(str,data)
    x = ""
    name = []
    country = []
    city = []
    rank = []
    api = {}
    for i in data:
        name.append(i[0])
        country.append(i[1])
        city.append(i[2])
        rank.append(i[3])
        id ={"name":i[0],"country":i[1],"city":i[2],"rank":i[3]}
        api.update({i[0]:id})
    # api = {"name":name,"country":country,"city":city,"rank":rank}
    # api = {"jsonarray":[api]}
    return jsonify(api)

@app.route('/ip/<ip>/<string:path>/', methods=['GET'])
def ip(ip,path):
    ips = 'http://ip-api.com/json/'+ ip +'?lang=zh-CN&fields=status,message,continent,country,regionName,city,isp,org,reverse,mobile,proxy,hosting,query'
    data = requests.get(ips)
    data = data.json()
    data = json.loads(json.dumps(data))
    f = open('/volume1/music/school.txt', 'a' , encoding='utf-8')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time = time.split()
    f.write(time[0] + "|" + time[1]+"|"+path)
    for i in data:
        f.write("|"+str(data[i]))
    f.write("\n")
    f.close()
    
    return jsonify(data)

# @app.route('/school', methods=['GET'])
# def school():
#     date = []
#     ip = []
#     f = open("/volume1/music/school.txt", 'r' , encoding='utf-8')
#     for line in f.readlines():
#         data = line.split("|")
#         if data[0] not in date:
#             date.append(data[0])
#             if data[len(data)-1] not in ip:
#                 ip.append(data[len(data)-1])

@app.route('/date1', methods=['GET'])
def date1():
    date = []
    x = datetime.datetime.now().strftime("%Y-%m-%d")
    for i in range(1,6):
        date.append(x)
        x = datetime.datetime.strptime(x, "%Y-%m-%d")
        x = x + datetime.timedelta(days=+1)
        x = x.strftime("%Y-%m-%d")
        image = Image.new('RGBA', (60, 10), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        color = 'rgb(0, 0, 0)'
        # font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 20)
        draw.text((0, 0), x, fill=color)
        image.save("/volume1/python/static/date/"+str(i)+".png")
    return "<img src='static/date/1.png'>"

@app.route('/date2', methods=['GET'])
def date2():
    return "<img src='static/date/2.png'>"
@app.route('/date3', methods=['GET'])
def date3():
    return "<img src='static/date/3.png'>"
@app.route('/date4', methods=['GET'])
def date4():
    return "<img src='static/date/4.png'>"
@app.route('/date5', methods=['GET'])
def date5():
    return "<img src='static/date/5.png'>"
# @app.route('/remove', methods=['GET'])
# def remove():
#     for i in range(1,6):
#         os.remove("/volume1/python/"+str(i)+".png")
#     return "remove"

# @app.route('/api', methods=['GET'])
# def txt():
#     data = ""
#     with open('/volume1/music/form.diff', 'r' , encoding='utf-8') as f:
#         data = f.read()
#     # f = open('/volume1/music/form.diff', 'r' , encoding='utf-8')
#     # for line in f.readlines():
        
#     #     data += line
        
#     # f.close()
#     # #print(data)
#     return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
