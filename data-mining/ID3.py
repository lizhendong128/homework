from math import log
import operator

def calcShannonEnt(dataSet):  # 计算数据的熵
    numEntries=len(dataSet)  # 数据条数
    labelCounts={} # 用于统计有多少个类以及每个类的数量
    
    for featVec in dataSet:
        currentLabel=featVec[-1] # 每行数据的最后一个字（类别）
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1  # 统计
        
    shannonEnt=0 # 熵
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries # 计算单个类的熵值
        shannonEnt-=prob*log(prob,2) # 累加每个类的熵值
    return shannonEnt


def createDataSet():    # 输入数据，
    # 样例：根据头发和声音来判断性别
    dataSet = [['长', '粗', '男'],
               ['短', '粗', '男'],
               ['短', '粗', '男'],
               ['长', '细', '女'],
               ['短', '细', '女'],
               ['短', '粗', '女'],
               ['长', '粗', '女'],
               ['长', '粗', '女']]
    labels = ['头发','声音']  #两个特征
    return dataSet,labels


def splitDataSet(dataSet,axis,value): # 按某个特征分类后的数据
    retDataSet=[]
    for featVec in dataSet: # 对于每一行数据
        if featVec[axis]==value: # 如果指定的列的值等于给定的数
            reducedFeatVec =featVec[:axis] # 得到此列之前的值
            reducedFeatVec.extend(featVec[axis+1:])# 加上之后的值，即把原来的数据集去掉此列
            retDataSet.append(reducedFeatVec) # 保存修改后的数据
    return retDataSet # 只包括了去除了特定值的行


def chooseBestFeatureToSplit(dataSet):  # 选择最优的分类特征
    numFeatures = len(dataSet[0])-1 # 数据中参考项（不包括最后一项）数量
    baseEntropy = calcShannonEnt(dataSet)  # 原始的熵
    bestInfoGain = 0 # 熵值减少的数量
    bestFeature = -1 # 保存最优分类特征
    for i in range(numFeatures):
        featList = [line[i] for line in dataSet] # 数据集中的第i列
        uniqueVals = set(featList) # 化成集合，去重
        newEntropy = 0 
        for value in uniqueVals: # 对于每一个种类
            subDataSet = splitDataSet(dataSet,i,value)
            prob =len(subDataSet)/float(len(dataSet)) # 去掉特定值的行数除以总行数
            newEntropy +=prob*calcShannonEnt(subDataSet)  # 按特征分类后的熵
        infoGain = baseEntropy - newEntropy  # 原始熵与按特征分类后的熵的差值
        if (infoGain>bestInfoGain):   # 若按某特征划分后，熵值减少的最大，则次特征为最优分类特征
            bestInfoGain=infoGain
            bestFeature = i
    
    return bestFeature


def majorityCnt(classList):    #按分类后类别数量排序，比如：最后分类为2男1女，则判定为男；
    classCount={} # 字典，用于保存各个类别的数量
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1 # 增加1
    #sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    sortedClassCount = sorted(classCount.items(),key=lambda p:p[1],reverse=True) # 根据数量进行排序
    
    return sortedClassCount[0][0] # 返回数量最多的类别


def createTree(dataSet,labels): # 创造决策树
    classList=[line[-1] for line in dataSet]  # 获取数据集里的最后一列（性别）
    
    if classList.count(classList[0])==len(classList): # 当数据集里性别相同时，返回这个性别
        return classList[0]
    
    if len(dataSet[0])==1: # 数据集中无特征项，返回数量最多的结果
        return majorityCnt(classList)
    
    bestFeat=chooseBestFeatureToSplit(dataSet) #选择最优特征
    bestFeatLabel=labels[bestFeat] # 获取最优特征标签
    myTree={bestFeatLabel:{}} #分类结果以字典形式保存
    del(labels[bestFeat]) # 删除分类了的标签，以便继续查找
    featValues=[line[bestFeat] for line in dataSet] # 获取数据集中的最优特征标签的列
    uniqueVals=set(featValues) # 去重
    for value in uniqueVals: # 
        subLabels=labels[:] # 获取标签
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels) # 递归，继续寻找
    return myTree



# 代码开始部分

dataSet, labels=createDataSet()  # 返回数据集和标签
myTree = createTree(dataSet, labels) # 生成决策树
print(myTree)  # 输出决策树模型结果
