from numpy import *
import pandas as pd


def distEclud(vecA, vecB): # 计算欧氏距离
    return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k): # 随机生成K个质心
    n = shape(dataSet)[1] # 读取数据的列数n
    centroids = mat(zeros((k,n)))# 生成k个含有n个0的列表（K行N列）
    for j in range(n):
        minJ = min(dataSet[:,j]) # 得到每一列中最小的值
        rangeJ = float(max(array(dataSet)[:,j]) - minJ) # 求出一列中最大和最小的差
        centroids[:,j] = minJ + rangeJ * random.rand(k,1) # 求出质心,rand(k,1)返回K*1维数组
        
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):  # k-means算法，
# 输入数据和k值。后面两个参数是可选的距离计算方式和初始质心的选择方式
    m = shape(dataSet)[0] # 读取数据的行数，即m个点
    clusterAssment = mat(zeros((m,2))) # 生成m*2的0，保存每个点属于哪个簇，以及到质心的距离
    centroids = createCent(dataSet, k) # 生成质心
    clusterChanged = True # 用于判断簇是否改变
    
    while clusterChanged: # 如果簇改变，需要继续计算
        clusterChanged = False # 改变flag
        for i in range(m):# 对于每一个点
            minDist = inf # 正无穷
            minIndex = -1 # 最小距离点的标号
            for j in range(k): # 对于每一个质心
                distJI = distMeas(centroids[j,:],dataSet[i,:]) # 计算某个点到所有质心的距离
                if distJI < minDist: # 保存最小距离及其质心
                    minDist = distJI
                    minIndex = j
                    
            if clusterAssment[i,0] != minIndex: # 如果发现这个点对应的质心改变，就说明簇改变
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2 # 更新簇记录
        
        for cent in range(k): # 根据簇重新计算质心
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]] # 得到簇中的所有的点
            centroids[cent,:] = mean(ptsInClust, axis=0) # 求均值，得到质心
    
    return centroids, clusterAssment



def draw(dataSet, k, centroids, clusterAssment): # 可视化结果
    from matplotlib import pyplot as plt  
    numSamples, dim = dataSet.shape  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    for i in range(numSamples):  
        markIndex = int(clusterAssment[i, 0])  
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    for i in range(k):  
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
    plt.show()



dataMat = mat(pd.read_csv('company.csv', encoding = 'gbk')) # 读取数据集
myCentroids, clustAssing= kMeans(dataMat,4) # k-means方法，得到
print(myCentroids)
draw(dataMat, 4, myCentroids, clustAssing)  


