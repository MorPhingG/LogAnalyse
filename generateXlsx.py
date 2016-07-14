import os, re, sys, xlsxwriter
fname="SUMMARY.md"

# try:
#     fobj = open(fname, 'r')
# except IOError, e:
#     sys.stderr.write("SUMMARY.md not found")
#     sys.exit(1)
# else:
fobj = open(fname, 'r')
print("\t".join(["event","property","property_type","description","title","filename"]))
for eachline in fobj:
    match1=re.search('\[([^\]]+)\]\(([^)]+)\)',eachline)
    if match1:
        [title,filename]=match1.groups()
        if os.path.exists(filename):
            fobj2=open(filename,'r')
            point=""
            skip=False
            for eachline2 in fobj2:
                # 跳过不用的表格部分
                if skip:
                    if re.match('--',eachline2):
                        skip=False
                    continue

                # 匹配埋点
                match2=re.match('>\s+埋点\s+([a-zA-z_]+)',eachline2)
                if match2:
                    [point]=match2.groups()
                    # print("\t".join([point, title, filename]))
                    skip=True
                    continue

                # 匹配属性表格
                if point:
                    match2=re.match('(\w+)\s*\|\s*(\w+)\s*\|\s*(.+)$',eachline2)
                    if match2:
                        [first,second,third]=match2.groups()
                        print("\t".join([point,first,second,third, filename, title]))
                    else:
                        point=""
            fobj2.close()
fobj.close()