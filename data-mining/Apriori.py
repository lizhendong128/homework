'''
输入items;
k=1;
计算出K(=1)项集
while(1)
    计算支持度并剪枝；
        判断K项集中的列表是否包含在items中的列表中
            计数，计算出支持度
            将支持度大于基准值的项保存下来，作为 频繁K项集
    将频繁K项集保存到all里
    if(频繁K项集为空):
        返回频繁k-1项集;
    else:
        k=k+1
    将频繁K项集进行连接，生成k+1项集;
'''


import copy

# 输入的items
items =[['A', 'B', 'C', 'D'], ['B', 'C', 'E'],
        ['A', 'B', 'C', 'E'], ['B', 'D', 'E'],
        ['A', 'B', 'C', 'D']] # 输入项集
minSup = 0.5    #最小支持度
k = 1   # 初始值k = 1
item1 = [] #用于保存1项集以及其他项集

for i in items: # 生成1项集
    for j in i:
        if [j] not in item1:
            item1.append([j])

##计算支持度
frequent_item_all = []   # 用于保存所有的频繁项集

while(1): #使用循环来进行多次操作
    #计算支持度，得到频繁项集
    # 判断K项集中的列表是否包含在items中的列表中
    frequent_item_k = []  # 保存频繁k项集
    for key in item1:  # 项集中的每一项
        temp = 0  # 用来保存每个项在items的匹配数量
        for item in items:  # 对于items中的每个项
            if (set(key).issubset(set(item))):  # 判断item是否包含key的内容
                temp += 1
        if temp * 1.0 / len(items) >= minSup:  # 判断项集的支持度是否大于最小支持度
            frequent_item_k.append(key)
            frequent_item_all.append(key)  # 保存这一项

    keys1 = copy.deepcopy(frequent_item_k)  # 使用deepcopy，将频繁项集保存到keys1
    frequent_item_k.clear()
    item1.clear()
    print(keys1)

    pass

    # 判断频繁K项集是否为空
    if len(keys1) == 0:
        # 如果为空，返回频繁K-1项集
        k = k - 1
        break

    # 将频繁K项集连接，生成K+1项集放在item1中，循环继续
    # 转换成集合，以此判断是否有K-1项相同，决定是否连接
    i = j = -1
    while i < len(keys1):
        i = i + 1
        j = i
        while(j < len(keys1) - 1):
            j = j + 1
            temp = list(set(keys1[i]).union(set(keys1[j])))
            temp.sort()
            if len(temp)==k+1 and list(temp) not in item1:
                item1.append(list(temp))
                print(item1)

    k = k + 1
# 输出k项集
print(frequent_item_all)
