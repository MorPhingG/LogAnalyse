import sqlite3
from flask import Flask, request
from preprocessing import *
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logList = getlog('boxfish-online-order-public.log')
logDict = toDict(logList)
logListInsert = toListForSql(logList, logDict)

app = Flask(__name__)

# cx = sqlite3.connect("./log.db")
# cu = cx.cursor()
# cu.execute("create table logOrder (id INTEGER PRIMARY KEY AUTOINCREMENT, createTime datetime, orderStatus varchar(30), userId int, "
#            "orderCode varchar(32) , orderInfo text) ")
# cu.execute("create index orderIndex on logOrder(createTime)")
# for t in logListInsert:
#     cx.execute("insert into logOrder values (NULL,?,?,?,?,?)", t)
# cx.commit()
# cu.execute("select * from logOrder")
# Fetch = cu.fetchall()
# cu.execute("drop table catalog")
# cx.commit()

# cu.execute("select top 1000 * from catalog order by time desc")

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
        # print(postId)
        cu.execute("select createTime, orderStatus, userId, orderCode, orderInfo from catalog where id=?",postId)
        cx.commit()
        result = to_json(cu.fetchall())
        return(result)
    print("hello")
    return app.send_static_file('LogAnalyse.html')

app._static_folder="static"

@app.route('/orders')
def orders():
    cx = sqlite3.connect("./log.db")
    cu = cx.cursor()
    cu.execute("select createTime, orderStatus, userId, orderCode, orderInfo from logOrder")
    return to_json(cu.fetchall())

@app.route('/orders/order', methods=['POST'])
def order():
    cx = sqlite3.connect("./log.db")
    cu = cx.cursor()
    cx.commit()
    userId = request.args.get('userId')
    userIdStr = str(userId)
    print(userId)
    print(userIdStr)
    # cu.execute("select * from logOrder where userId=?", userId)
    cu.execute("select createTime, orderStatus, userId, orderCode, orderInfo from logOrder where (userId=" + userId + ") or (orderCode=" + "'"+userIdStr+"')")
    cx.commit()
    result = to_json(cu.fetchall())
    return(result)

if __name__ == "__main__":
    app.run(debug=True)



