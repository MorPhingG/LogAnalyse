import re
import xlrd
import json

# get log
def getlog(filename):
    allText = open(filename).read( )
    reg = r'([^\]]+][^\[]+)\[EVENT\]([\w]+)\s*({.+)'
    logRe = re.compile(reg)
    logList = re.findall(logRe,allText)
    return logList

# read .xlsx file
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
    return p

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
        logListInsert[i].append(logDict[i]['orderStatus'])
        logListInsert[i].append(logDict[i]['userId'])
        logListInsert[i].append(logDict[i]['orderCode'])
        logListInsert[i].append(str(logDict[i]))
    return logListInsert

def to_json(data):
    if data==[]:
        return 0
    print(data)
    Dict = [{} for i in range(len(data))]
    head = ["createTime", "orderStatus", "userId", "orderCode", "orderInfo"]
    for i in range(len(data)):
        Dict[i] = dict(map(lambda a,b:[a,b], head, data[i]))
    return json.dumps(Dict)

# logListT = read_xlsx('logOrder.xlsx')