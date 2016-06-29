import re
import sqlite3
import json
import xlrd
from flask import Flask, request
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

def read_xlsx(filename):
    workbook = xlrd.open_workbook(filename)
    booksheet = workbook.sheet_by_index(3)
    p = []
    for row in range(booksheet.nrows):
            row_data = []
            for col in range(booksheet.ncols):
                    cel = booksheet.cell(row, col)
                    val = cel.value
                    try:
                            val = cel.value
                            val = re.sub(r'\s+', '', val)
                    except:
                            pass

                    if type(val) == float:
                        val = int(val)
                    else:
                        val = str( val )
                    row_data.append(val)
            p.append(row_data)
    return  p

# change str to dic
def toDict(logList):
    logDict = [{} for i in range(len(logList))]
    for i in range(len(logList)):
        logDict[i] = eval(logList[i][2])
    return logDict

def toListForSql(logList,logDict):
    logListInsert = [[] for i in range(len(logList))]
    for i in range(len(logList)):
        logListInsert[i].append(logDict[i]['createTime'])
        logListInsert[i].append(logList[i][1])
        logListInsert[i].append(logDict[i]['userId'])
        logListInsert[i].append(logDict[i]['orderCode'])
        logListInsert[i].append(str(logDict[i]['orderDetails']))
    return logListInsert

# logListT = read_xlsx('logOrder.xlsx')

logList = getlog('boxfish-online-order-public.log')
logDict = toDict(logList)
logListInsert = toListForSql(logList, logDict)

app = Flask(__name__)

# cx = sqlite3.connect("./test.db")
# cu = cx.cursor()
# cu.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
# cu.execute("create index orderIndex on catalog(id)")
# for t in[(0,10,'abc','Yu'),(1,20,'cba','Xu'),(2,30,'kda','solo'),(3,20,'gpa','carry'),(4,25,'cfa','safe'),(5,40,'nba','jungle')]:
#     cx.execute("insert into catalog values (?,?,?,?)", t)
# cx.commit()
# cu.execute("select * from catalog")
# cu.fetchall()
# cu.execute("drop table catalog")
# cx.commit()

# cx = sqlite3.connect("./log.db")
# cu = cx.cursor()
# cu.execute("create table logOrder (createTime datetime, type varchar(30), userId int, "
#            "orderCode varchar(32) , orderDetails text PRIMARY KEY) ")
# cu.execute("create index orderIndex on logOrder(createTime)")
# for t in logListInsert:
#     cx.execute("insert into logOrder values (?,?,?,?,?)", t)
# cx.commit()
# cu.execute("select * from logOrder")
# Fetch = cu.fetchall()
# cu.execute("drop table catalog")
# cx.commit()


# cu.execute("select top 1000 * from catalog order by time desc")

def to_json(data):
    if data==[]:
        return 0
    print(data)
    Dict = [{} for i in range(len(data))]
    head = ["createTime", "type", "userId", "orderCode", "orderDetails"]
    for i in range(len(data)):
        Dict[i] = dict(map(lambda a,b:[a,b], head, data[i]))
    return json.dumps(Dict)

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
        # print(postId)
        cu.execute("select * from catalog where id=?",postId)
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
    cu.execute("select * from logOrder")
    return to_json(cu.fetchall())

@app.route('/orders/order', methods=['POST'])
def order():
    cx = sqlite3.connect("./log.db")
    cu = cx.cursor()
    cx.commit()
    userId = request.args.get('userId')
    # cu.execute("select * from logOrder where userId=?", userId)
    cu.execute("select * from logOrder where userId=" +userId)
    cx.commit()
    result = to_json(cu.fetchall())
    return(result)

if __name__ == "__main__":
    app.run(debug=True)



