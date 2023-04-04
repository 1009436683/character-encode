import fitz   #PyMuPDF
from xpinyin import Pinyin  #xpinyin
import numpy as np
import seaborn as sns
from sklearn import preprocessing  #scikit-learn
import operator
import json

file_path = "C:/Users/10094/Desktop/高效均匀的打字编码方法/共产党宣言.pdf"
doc = fitz.open(file_path)
p = Pinyin()
spellDict={} #存储各读音出现的次数
for page in doc:
    text = page.get_text("text")
    for c in text:
        if '\u4e00' <= c <= '\u9fff':
            ch=p.get_pinyin(c,'')
            if ch in spellDict:
                spellDict[ch]+=1
            else :
                spellDict[ch]=1
sortedSpellDict=dict(sorted(spellDict.items(), key=operator.itemgetter(1)))
#重新编码
class Node:
    def __init__(self,key,freq):
        self.key = key #节点的名字
        self.freq = freq
        self.child = {} #节点孩子
        self.code = ''
def create_nodeQ(p_dict):
    Q=[]
    for i in p_dict.keys():
        Q.append(Node(i,p_dict[i]))  
    Q.sort(key=lambda item:item.freq,reverse = True)  #用lambda隐函数实现队列按照字母的概率降序排列      
    return Q 
def addQ(Q, nodeNew):
  if len(Q) == 0:
    return [nodeNew]
  else:
      Q=Q+[nodeNew]
      Q.sort(key=lambda item:item.freq,reverse=True)
      #每次加入节点都需要重新排列成降序
  return Q
class Nodequeue:
    def __init__(self,p_dict):
        self.que = create_nodeQ(p_dict)
        self.size = len(self.que)
        
    def addnode(self,node):
        self.que = addQ(self.que, node)
        self.size += 1
       
    def popNode(self):
        self.size -= 1
        return self.que.pop()
    #加入队列长度要+1，弹出长度-1
def creatHuffmanTree(nodeQ,exact_division):
  if exact_division == True:
      w=0
      for i in range(1,24):
         locals()['node_'+str(i)]=nodeQ.popNode()
         w+=locals()['node_'+str(i)].freq
      r = Node(None,w)
      for i in range(1,24):
        r.child[i] = locals()['node_'+str(i)]
      nodeQ.addnode(r)
  while nodeQ.size != 1:
    w=0
    for i in range(1,26):
       locals()['node_'+str(i)]=nodeQ.popNode()
       w+=locals()['node_'+str(i)].freq
    r = Node(None, w)
    for i in range(1,26):
       r.child[i]=locals()['node_'+str(i)]
    nodeQ.addnode(r)
  return nodeQ.popNode()
  #最后返回的是队列的最后一个节点，也就是概率最大的点，就是这个huffman树的根节点

#由树得到编码表
codeDic1 = {}#编码字典
# 由哈夫曼树得到哈夫曼编码表
def HuffmanCodeDic(roof, x):
  global codeDic, codeList
  if roof:#只要根不为空
    for i in range(1,26):
       if i in roof.child:
          HuffmanCodeDic(roof.child[i],x+chr(96+i))
    roof.code += x
    if roof.key:
      codeDic1[roof.key] = roof.code

# 字符串编码
def TransEncode(string):
  global codeDic1
  transcode = ""
  for i in string:
    transcode += codeDic1[i]
  return transcode
exact_division=True
t = Nodequeue(sortedSpellDict)
tree = creatHuffmanTree(t,exact_division)
HuffmanCodeDic(tree, '') #从哈夫曼树获取编码
with open("C:/Users/10094/Desktop/高效均匀的打字编码方法/codeDict.json", "w", encoding='utf-8') as f:
    json.dump(codeDic1,f, indent=2, sort_keys=True)   #保存结果
#用新的编码得到新的拼音字典
newSpellDict={}
#计算新的编码的数据评价
for c in spellDict:
   newSpellDict[codeDic1[c]]=spellDict[c]
newLetterDict={} #获得新的字母使用情况
for i in range(97,123):
    newLetterDict[chr(i)]=0
for ch in newSpellDict:
   for c in ch:
      newLetterDict[c]+=newSpellDict[ch]
keys=['a','s','d','f','j','k','l']  #一般情况下手指放置的按键
otherKeys=['q','w','e','r','t','y','u','i','o','p','g','h','z','x','c','v','b','n','m']
list1=[]
list2=[]
for c in keys:
    list1.append(newLetterDict[c])
for c in otherKeys:
    list2.append(newLetterDict[c])  #将按键频率分为两个维度进行计算
#计算按键使用均衡性
array1=np.asarray(list1).reshape(-1,1)
array2=np.asarray(list2).reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
array1_minMax = min_max_scaler.fit_transform(array1)
array2_minMax = min_max_scaler.fit_transform(array2)
s=np.std(array1_minMax)+np.std(array2_minMax) #两个维度的标准差之和作为均衡性的标准
print("按键使用均衡性即标准差为：",s)
typeNum=0 #按键次数
for c in newLetterDict:
   typeNum+=newLetterDict[c]
characterNum=0 #汉字字数
for ch in spellDict:
   characterNum+=spellDict[ch]
typeTime=0 #打字时间
timeDict={} #字母耗时字典
for c in keys:
    timeDict[c]=0.5 #手指位置的按键更容易点击
for c in otherKeys:
    timeDict[c]=0.8 
for c in newLetterDict:
   typeTime+=timeDict[c]*newLetterDict[c]
print("总按键次数为：",typeNum)
print("汉字总数为：",characterNum)
print("平均单字按键数：",typeNum/characterNum)
print("平均单字耗时：",typeTime/characterNum)
#绘制热力图
a=[]
for i in range(97,123):
    a.append(newLetterDict[chr(i)])
array = np.asarray(a)
x_ticks = []
for i in range(97,123):
    x_ticks.append(chr(i))
y_ticks = ['']  # 自定义横纵轴
ax = sns.heatmap([array], xticklabels=x_ticks, yticklabels=y_ticks,cmap="YlGnBu")
ax.set_title('NewHeatmap')  # 图标题
ax.set_xlabel('letters')  # x轴标题
ax.set_ylabel('')