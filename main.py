import sqlite3
from flask import Flask, request
from preprocessing import *
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logList = getlog('boxfish-online-order-public.log')
logDict = toDict(logList)
logListInsert = toListForSql(logDict)

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

app = Flask(__name__)
app._static_folder="static"


@app.route('/')
def index():
    return app.send_static_file('LogAnalyse.html')

@app.route('/<int:pageIndex>')
def indexPagination(pageIndex):
    return app.send_static_file('LogAnalyse.html')

@app.route('/orders', methods=['POST'])
def orders():
    cx = sqlite3.connect("./log.db")
    cu = cx.cursor()
    cu.execute("select createTime, orderStatus, userId, orderCode, orderInfo from logOrder ORDER BY createTime DESC")
    dataSqlite = cu.fetchall()
    if request.method == "POST":
        pageIndex = int(request.args.get('pageIndex',1))
        print(pageIndex*10-10)
        print(pageIndex*10)
        return toJson(dataSqlite[pageIndex*10-10:pageIndex*10])
    # return toJson(dataSqlite)

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
    result = toJson(cu.fetchall())
    return(result)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

