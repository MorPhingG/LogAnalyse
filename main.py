import re
import sqlite3
from flask import Flask, request
import json
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# get log
def getlog(filename):
    allText = open(filename).read( )
    reg = r'([^\]]+][^\[]+)\[EVENT\]([\w]+)\s*({.+)'
    logRe = re.compile(reg)
    logList = re.findall(logRe,allText)
    return logList

logList = getlog('LogOrder.csv')

app = Flask(__name__)

cx = sqlite3.connect("./test.db")
cu = cx.cursor()
# cu.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
# cu.execute("create index orderIndex on catalog(id)")
# for t in[(0,10,'abc','Yu'),(1,20,'cba','Xu'),(2,30,'kda','solo'),(3,20,'gpa','carry'),(4,25,'cfa','safe'),(5,40,'nba','jungle')]:
#     cx.execute("insert into catalog values (?,?,?,?)", t)
cx.commit()
cu.execute("select * from catalog")
cu.fetchall()
# cu.execute("drop table catalog")
# cx.commit()

# cu.execute("select top 1000 * from catalog order by time desc")

def to_json(data):
    if data==[]:
        return 0
    print(data)
    Dict = [{} for i in range(len(data))]
    head = ["id", "pid", "name", "nickname"]
    for i in range(len(data)):
        Dict[i] = dict(map(lambda a,b:[a,b], head, data[i]))
    return json.dumps(Dict)

@app.route('/orders')
def orders():
    cx = sqlite3.connect("./test.db")
    cu = cx.cursor()
    cu.execute("select * from catalog")

    return to_json(cu.fetchall())
#
# @app.route('/orders', methods = ['GET'])
# def getOrder():
#     cx = sqlite3.connect("./test.db")
#     cu = cx.cursor()
#     cu.execute("select * from catalog")
#     return
#
# @app.route('/orders/order/<int:post_id>', methods = ['GET'])
# def getOrderYouWant(post_id):
#     cx = sqlite3.connect("./test.db")
#     cu = cx.cursor()
#     cu.execute("select * from catalog where id = ?" , post_id)
#     return

@app.route('/', methods=['POST','GET'])
def index():
    if(request.method=="POST"):
        cx = sqlite3.connect("./test.db")
        cu = cx.cursor()
        cx.commit()
        postId = request.form.get('searchQuery','0')
        cu.execute("select * from catalog where id=?",postId)
        cx.commit()
        result = to_json(cu.fetchall())
        return(result)
    print("hello")
    return app.send_static_file('LogAnalyse.html')

app._static_folder="static"

@app.route('/orders/order', methods=['POST'])
def order():
    cx = sqlite3.connect("./test.db")
    cu = cx.cursor()
    cx.commit()
    id = request.args.get('id')
    cu.execute("select * from catalog where id=?", id)
    cx.commit()
    result = to_json(cu.fetchall())
    return(result)

if __name__ == "__main__":
    app.run(debug=True)



