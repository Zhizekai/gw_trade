#import pytesseract
#coding:utf-8
import os, sys
import re
#import Image
import numpy as np
import pandas as pd

from datetime import *

t1 = date(2016, 8, 3)
t2 = datetime(2016, 8, 3)

if t1 == t2:
    print("time equal")

print(t2-t1)
pd_id = "109554";
pd_key = "1Yd5+vpvVROCSLickrtTx3CdKkqsi1GN";
app_id = "309554";
app_key = "aTyjQwZwQ0PFhBcgPuebJeEFP9KCHi/0";
# 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
pred_type = "50100";
# 初始化api接口

'''''

dict_ins = {"a":"1111", "b":"2222"}
str='     '.join('{}:{}'.format(k, v) for k, v in dict_ins.items())
print(str)


for i in range(5):
    print("i=", i)
exit()

def get_last_month(month_day):
    s1 = "20" + month_day
    d1 = datetime.strptime(s1, "%Y%m")
    d2 = d1 - timedelta(days=1)
    return d2.strftime("%Y%m")
d2 = get_last_month("1609")


exit()

a = np.array([-1,  -1 ,  -1,  -1,  -1])
print(a/2)
print(abs(a).mean())


t1 = date(2016, 8, 3)
t2 = datetime(2016, 8, 3)

if t1 == t2:
    print("time equal")

print(t2-t1)

data = {
      'closePrice': np.array([ 16.93,  16.3 ,  16.56,  16.95,  16.66]),
      'turnoverValue': np.array([  4.44733303e+09,   5.77643795e+09,   3.94335705e+09, 4.64033583e+09,   3.89352207e+09]),
      'turnoverVol': np.array([  2.60952337e+08,   3.44725740e+08,   2.41593696e+08, 2.77314172e+08,   2.31968840e+08]),
      'lowPrice': np.array([ 16.8 ,  16.16,  15.98,  16.5 ,  16.56]),
      'highPrice': np.array([ 17.5 ,  17.2 ,  16.7 ,  16.98,  17.04]),
      'openPrice': np.array([ 17.5 ,  17.1 ,  16.32,  16.58,  16.98])
  }

a = [1 if data['closePrice'][i] - data['openPrice'][i] >= 0 else 0 for i in range(5)]
print(sum(a))



exit()


a=(1, 2, 3)
print(a)
b=['黑莓手机一代','黑莓手机二代']
mob = ['魅族手机', b,'锤子手机']
print(mob)

exit()
def get_vcode(vcode_file, decode_file):
    cmd = r'"D:\Program Files\Tesseract-OCR\tesseract.exe "' + " " +  vcode_file + " " + decode_file
    print(cmd)
    os.system(cmd)
    f = open(decode_file+".txt", 'r')
    tmp_line = f.readline().strip()
    return tmp_line

if len(sys.argv) < 2:
    print 'Usage: ./test.py file_name'
    sys.exit()
file_name=sys.argv[1]
print get_vcode(r"d:\1.jpg", r"d:\vcode")

x=-6/13
print(x)


n = 2
m = 3
matrix = [None]*2
#for i in range(len(matrix)):
#    matrix[i] = [0]*3

#matrix[0][1] = 123
#matrix[0].append(1233)
#print(matrix)

#exit()
test_str = u"alert aaa12312.2。" \
           u"alert aaa12312"
'''''

test_str = 'alert("-990297020[-990297020] '
#
reg = re.compile('.*alert.*\[-(\d{6,})\].*')
#reg = re.compile(u'alert.*?(\d+\.\d*)')
match = reg.search(test_str)
if match:
    #reg = re.compile(ur'\d{4,}')
    print(match.group(1))

def sample():
    (ret, data) = getSomething()
    if ret == 1 or ret == 2:
        print("getSomething error: ret=%d", ret)
        return

    #ret ok, # process data
    processData(data)

def sample():
    (ret, data) = getSomething()
    if ret == 1 or ret == 2:
        print("getSomething error: ret=%d", ret)
        return -10
    if ret == 3:
        #do something
        doSomething()
        return -20

    #ret ok, # process data
    processData(data)

    return 0


def sample():
    (ret, data) = getSomething()
    if ret == 0:
        # ret ok, # process data
        processData(data)
        return 0
    elif ret == 3:
        doSomething()
        return -10
    else:
        print("getSomething error: ret=%d", ret)
        return -20

