import json
import numpy as np
from sklearn import preprocessing  #scikit-learn
import fitz   #PyMuPDF
from xpinyin import Pinyin  #xpinyin

with open('C:/Users/10094/Desktop/高效均匀的打字编码方法/dict.json', 'r') as fp:
    letterDict = json.load(fp)  #读取字母使用次数
keys=['a','s','d','f','j','k','l']  #一般情况下手指放置的按键
otherKeys=['q','w','e','r','t','y','u','i','o','p','g','h','z','x','c','v','b','n','m']
list1=[]
list2=[]
for c in keys:
    list1.append(letterDict[c])
for c in otherKeys:
    list2.append(letterDict[c])  #将按键频率分为两个维度进行计算
#计算按键使用均衡性
array1=np.asarray(list1).reshape(-1,1)
array2=np.asarray(list2).reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
array1_minMax = min_max_scaler.fit_transform(array1)
array2_minMax = min_max_scaler.fit_transform(array2)
s=np.std(array1_minMax)+np.std(array2_minMax) #两个维度的标准差之和作为均衡性的标准
print("按键使用均衡性即标准差为：",s)

#计算输入效率
typeNum=0 #按键次数
characterNum=0 #汉字字数
typeTime=0 #打字时间
timeDict={} #字母耗时字典
for c in keys:
    timeDict[c]=0.5 #手指位置的按键更容易点击
for c in otherKeys:
    timeDict[c]=0.8 
file_path = "C:/Users/10094/Desktop/高效均匀的打字编码方法/共产党宣言.pdf"
doc = fitz.open(file_path)
p = Pinyin() 
for page in doc:
    text = page.get_text("text")
    for c in text:
        if '\u4e00' <= c <= '\u9fff':
            characterNum+=1
    pinyintext = p.get_pinyin(text,'')
    for c in pinyintext:
        if 'a'<= c <='z':
            typeNum+=1
            typeTime+=timeDict[c]
print("总按键次数为：",typeNum)
print("汉字总数为：",characterNum)
print("平均单字按键数：",typeNum/characterNum)
print("平均单字耗时：",typeTime/characterNum)