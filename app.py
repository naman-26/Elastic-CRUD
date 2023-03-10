from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import logging
import random

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
consoleHandler=logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
fileHandler = logging.FileHandler('record.log')
fileHandler.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s : %(name)s : %(levelname)s :%(message)s : %(Ip)s: %(method)s : %(endpoint_url)s : %(user_agent)s : %(Status)s', datefmt= '%d/%m/%Y %I:%M:%S')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
es = Elasticsearch(hosts=['http://127.0.0.1:9200/'])

def getIp():
    ip = ['91.231.240.165', '238.224.39.26', '83.193.195.41', '34.106.142.227', '165.248.188.228', '78.236.246.4', '143.69.195.221', '12.70.54.214', '5.60.83.253', '77.23.210.216', '68.205.137.143', '95.100.141.198', '162.197.79.242', '209.155.130.34', '228.160.135.72', '105.80.3.225', '34.117.247.80', '61.200.149.154', '27.3.69.168', '157.62.221.78', '32.138.51.234', '109.39.81.94', '128.211.159.43', '115.42.113.48', '76.6.108.251', '168.82.208.200', '172.124.188.86', '142.9.203.143', '163.130.184.8', '240.153.163.232', '239.137.78.5', '228.59.31.64', '172.107.70.71', '216.243.32.44', '145.163.133.131', '36.47.45.74', '45.181.58.59', '01.189.164.182', '225.106.112.103', '216.186.101.147', '144.123.104.164']
    idx = random.randint(0,len(ip)-1)
    return ip[idx]


def getUserAgent():
    UserAgent = ["Mozilla/5.0", "Chrome/4.0","Safari/6.0","Postman/7.1","Brave/2.0"]
    idx = random.randint(0,len(UserAgent)-1)
    return UserAgent[idx]

app = Flask(__name__)
@app.route('/',methods=['POST','PUT','GET','DELETE','PATCH'])
def home():
    if(request.method=='GET'):
        logger.info("-",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
        return ''' PATHs:
                        1)for insert : "/insert_data"
                        2)for update : "/update_data"
                        3)for delete : "/delete_data"
                        4)for search : "/search"
                        5)for searching all data : "/search_all"'''
    else:
        logger.error("-",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "BAD REQUEST"
    
if __name__ == "main":
    app.run(port=5000,debug=True)


# Insert
@app.route('/insert_data', methods=['POST','PUT','GET','DELETE','PATCH'])
def insert_data():
    
    if(request.method =='POST' or request.method == 'PUT'):
        if not request.form:
            logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
            return "Body Required"
        else:
            title = request.form['title']
            author = request.form['author']
            category = request.form['category']        
            blog = request.form['blog']
            blogNo = int(request.form['blogNo'])
            search_body={
                "query": {
                    "match": {
                        "blogNo": blogNo
                    }
                }
            }
            res=es.search(index="blogs", body=search_body)
            if res['hits']['hits']:
                logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
                return "Insert not possible data already exist\n Are you trying to update? (use /update_data)"
            else:
                insert_body = {
                    'blogNo' : blogNo,
                    'author': author,
                    'title': title,
                    'category': category,
                    'blog': blog,
                    'date': datetime.now()
                }
                result = es.index(index='blogs', id=blogNo, body=insert_body)
                logger.info("Success",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
                return str(result)
    else:
        logger.error("Wrong Method",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "Wrong Method"
    

# Update
@app.route('/update_data', methods=['POST','PUT','GET','DELETE','PATCH'])
def update_data():
    if request.method == 'POST' or request.method == 'PUT':
        if not request.form:
            logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
            return "Body Required"
        else:
            title = request.form['title']
            author= request.form['author']
            category=request.form['category']
            blog = request.form['blog']
            blogNo= int(request.form['blogNo'])
            search_body={
                "query": {
                    "match": {
                        "blogNo": blogNo
                    }
                }
            }
            res=es.search(index="blogs", body=search_body)
            if not res['hits']['hits']:
                logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
                return "update not possible data does not exist"
            else:
                update_body = {
                    'blogNo' : blogNo,
                    'author': author,
                    'title': title,
                    'category': category,
                    'blog': blog,
                    'date': datetime.now()
                }
                result = es.index(index='blogs', id=blogNo, body=update_body)
                logger.info("Success",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
                return str(result)
    else:
        logger.error("Wrong Method",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "Wrong Method"
    

# Search
@app.route('/search', methods=['POST','PUT','GET','DELETE','PATCH'])
def search():
    if request.method == 'GET':
        if not request.form:
            logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
            return "Search Field Required"
        else:
            keyword = request.form['keyword']
            field=request.form['field']
            body = {
                "query": {
                    "match": {
                        field: keyword
                    }
                }
            }
            res = es.search(index="blogs", body=body)
            logger.info("Success",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
            return str(res['hits']['hits'])
    else:
        logger.error("Wrong Method",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "Wrong Method"
    

# Search_all
@app.route('/search_all', methods=['POST','PUT','GET','DELETE','PATCH'])
def search_all():
    if request.method == 'GET':
        res = es.search(index="blogs")
        logger.info("Success",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
        return str(res)
    else:
        logger.error("Wrong Method",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "Wrong Method"
    

# Delete
@app.route('/delete_data', methods=['POST','PUT','GET','DELETE','PATCH'])
def delete_data():
    if request.method == 'DELETE':
        if not request.form:
            logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
            return "Id Field Required"
        else:
            blogNo= int(request.form['blogNo'])
            search_body={
                "query": {
                            "match":{
                                        "blogNo": blogNo
                                    }
                        }
                }
            res=es.search(index="blogs", body=search_body)
            if  not res['hits']['hits']:
                logger.error("Bad Request",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"400","method":request.method})
                return "delete not possible data does not exist"
            else:
                result = es.delete(index='blogs', id=blogNo)
                logger.info("Success",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"200","method":request.method})
                return str(result)
    else:
        logger.error("Wrong Method",extra={'Ip':getIp(),"endpoint_url":'/'+str(request.endpoint),"user_agent":str(getUserAgent()),"Status":"405","method":request.method})
        return "Wrong Method"

