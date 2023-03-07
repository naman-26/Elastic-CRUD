from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=['http://127.0.0.1:9200/'])

app = Flask(__name__)

@app.route('/')
def home():
     return ''' PATHs: 
                       1)for insert : "/insert_data"
                       2)for update : "/update_data"
                       3)for delete : "/delete_data"
                       4)for search : "/search"
                       5)for searching all data : "/search_all"'''


if __name__ == "main":
    app.run(port=5000,debug=True)


# Insert 

@app.route('/insert_data', methods=['POST','PUT'])
def insert_data():
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
    if res['hits']['hits']:
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
        return str(result)


# Update

@app.route('/update_data', methods=['POST','PUT'])
def update_data():
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
        return str(result)


# Search

@app.route('/search', methods=['GET','POST'])
def search():
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

    return str(res['hits']['hits'])

# Search_all

@app.route('/search_all', methods=['GET'])
def search_all():
    res = es.search(index="blogs")

    return str(res['hits']['hits'])


# Delete

@app.route('/delete_data', methods=['DELETE'])
def delete_data():
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
        return "delete not possible data does not exist"

    else:

        result = es.delete(index='blogs', id=blogNo)
        return str(result)

