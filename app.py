from flask import Flask, request, jsonify, render_template
import cv2
import time
import base64
from io import BytesIO
from flask_cors import CORS
import pymysql
from datetime import datetime
app = Flask(__name__)
from PIL import Image
import numpy as np
from yoloDetect import *

db = pymysql.connect(host='192.168.31.11',user='root',password='Zhanghuanjia1',port=3306,database='fjj',autocommit=True,charset='utf8')

CORS(app)  # 启用全局 CORS 支持
@app.route('/')
def hello_world():  # put application's code here


    return render_template('index3.html')
@app.route('/imgDetect',methods=['POST'])
def imgDetect():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    try:
        file = request.files['file'].read()
        #print(file)

        img = cv2.imdecode(np.frombuffer(file, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        #cv2.imshow('img', img)
        #cv2.waitKey(0)
        cv2.imwrite(f'imgs/{time.time()}_img.jpg', img)

        return jsonify({'status': 'ok',}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400



@app.route('/imgPredict2',methods=['POST'])
def imgPredict2():
    try:

        # Get the JSON data from the POST request
        data = request.get_json()

        # Extract the base64 image string from the request
        base64_image = data.get('image')

        # Decode the base64 string into binary data
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))

        # Perform your model prediction here
        # For now, let's simulate sending the image to a model server for prediction
        # You might want to send the image to another API or use a local model

        # Convert image to base64 string to return as prediction
       # timeId=base64.encode(time.time())
        #print(timeId)
        predicted_image_url = simulate_prediction(image)
        # Return the result
        return jsonify({'predicted_image_url': predicted_image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/getHistoryImg',methods=['GET'])
def getHistoryImg():

    try:
        cursor = db.cursor()
        page=int(request.args.get('page'))
        pageSize=int(request.args.get('pageSize'))
        #sql=f'select * from jilu LIMIT {(page-1)*pageSize}, {pageSize} '
        #sql = f'select imgId,originImgUrl,detectImgUrl,numOfBoxes,createTime from jilu LIMIT {(page - 1) * pageSize}, {pageSize} order by 5 '
        sql = f'select * from jilu order by 5 desc LIMIT {(page - 1) * pageSize}, {pageSize}  '
        cursor.execute(sql)
        rows = cursor.fetchall()
        res=[]
        for i in rows:
            res.append({'oriImg':i[1],'detectImg':i[2],'boxNum':i[3],'createTime':i[4]})
        print(res)
        cursor.close()
        return jsonify({'records':res}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400


def simulate_prediction(image):
    # Here, you can save the image or generate a new predicted image
    # In this case, we will simulate a "predicted image" by returning a placeholder URL
    # In real life, this would be replaced with the actual model prediction result
    try:
        cursor = db.cursor()
        id=base64.b64encode(str(time.time())[10:14].encode('utf-8')).decode()
        #id=str(time.time())[5:14]
        print(id)

        urlOri=f"http://192.168.31.11:5000/static/imgs/predicted{id}image.png"
        urlDetect=f"http://192.168.31.11:5000/static/dtImgs/predicted{id}image.png"
        #image.save(f"static/dtImgs/predicted{id}image.png")
        image.save(f"static/imgs/predicted{id}image.png")
        img=cv2.imread(f"static/imgs/predicted{id}image.png")
        decImg,boxes=getYoloResult(img)
        print(boxes)
        cv2.imwrite(f"static/dtimgs/predicted{id}image.png",decImg)
        #print(time.time())
        sql=f"insert into jilu(imgId,originImgUrl,detectImgUrl,numOfBoxes,createTime) values(\'{id}\',\'{urlOri}\',\'{urlDetect}\',{boxes.shape[0]},\'{datetime.now()}\')"
        #if boxes.shape[0]:
           #sqlbx="insert into boxes()"
        cursor.execute(sql)
        return urlDetect

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
