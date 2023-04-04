import fitz   #PyMuPDF
from xpinyin import Pinyin  #xpinyin
import json

file_path = "C:/Users/10094/Desktop/高效均匀的打字编码方法/共产党宣言.pdf"
doc = fitz.open(file_path)
p = Pinyin() 
resultDict={}
for i in range(97,123):
    resultDict[chr(i)]=0 #初始化字母字典
for page in doc:
    text = page.get_text("text")   #提取带换行符的纯文本
    pinyintext = p.get_pinyin(text,'')  #汉字转换为拼音
    for c in pinyintext:
        if c>='a' and c<='z':
            resultDict[c]+=1
with open("C:/Users/10094/Desktop/高效均匀的打字编码方法/dict.json", "w", encoding='utf-8') as f:
    json.dump(resultDict,f, indent=2, sort_keys=True)   #保存结果
print(resultDict)

#绘制热力图
import numpy as np
import seaborn as sns
a=[]
for i in range(97,123):
    a.append(resultDict[chr(i)])
array = np.asarray(a)
x_ticks = []
for i in range(97,123):
    x_ticks.append(chr(i))
y_ticks = ['']  # 自定义横纵轴
ax = sns.heatmap([array], xticklabels=x_ticks, yticklabels=y_ticks,cmap="YlGnBu")
ax.set_title('Heatmap')  # 图标题
ax.set_xlabel('letters')  # x轴标题
ax.set_ylabel('')