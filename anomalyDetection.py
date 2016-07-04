from preprocessing import *
logList = getlog('boxfish-online-order-public.log')
# logDict = toDict(logList)
# n=0
# for key, value in logDict[0].items():
#     # n=n+1
#     # print(n)
#     print(key, value)

text = logList[0][2]
orderInfo = {}
orderKey = []
keyBegin = 0
keyEnd = 0
flagLocateKey = 0
for i in range(len(text)):
    if(flagLocateKey == 0 and text[i] == '"'):
        keyBegin = i
        flagLocateKey = 1
    if(flagLocateKey == 1 and text[i] == '"'):
        KeyEnd = i
        orderKey.append(text[keyBegin+1:keyEnd])

