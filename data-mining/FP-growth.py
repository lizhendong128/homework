'''
# 先建树
第一次扫描，删去不频繁选项，得到过滤后的数据集
第二次扫描，建个树
寻找频繁项集
'''

'''
输入items
for item in items:
    记录元素出现的次数
for item in items:
    items和满足支持度的集合取交集，得到过滤后的数据
造树
for item in items:
    添加元素到树里
检测频繁项集
'''

def createTree(items, min_s):
    item_great = []     # 保存频繁元素
    headerTable = {}    # 字典，用来保存出现字符的次数
    min_support = min_s     # 最小支持度
    reserve_items = []  # 保存过滤后的元素

    # 计数
    for item in items:
        for ch in item:
            if ch not in headerTable:
                headerTable[ch] = 1
            else:
                headerTable[ch] += 1

    # 得到频繁的元素
    lessThanMinsup = []
    for v in headerTable:
        if headerTable[v] < min_support:  # 如果元素不频繁，加入列表
            lessThanMinsup.append(v)
    for v in lessThanMinsup:  # 删掉不频繁的元素
        headerTable.pop(v)

    if(len(headerTable.keys())==0):
        return None, None

    # 过滤数据集
    for item in items:
        temp = list(set.intersection(set(item), set(headerTable.keys())))  # 频繁的元素和数据集取交集
        orderedItems = sorted(temp, key=lambda p: (headerTable[p], p), reverse=True)  # 排序，根据出现次数以及字典顺序
        reserve_items.append(orderedItems)  # 加入新的列表中

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # 更新数据结构

    # 打印频繁项
    # print(reserve_items)

    # 建树
    tree = TreeNode('Null Set', 1, None)
    for item in reserve_items:  # 更新节点
        updateTree(item, tree, headerTable, count=1)

    # 打印树结构
    # tree.print_self()
    tree.item_great = reserve_items
    return tree, headerTable




def updateTree(items, InTree, headerTable, count):
    # 更新树
    if items[0] in InTree.children:  # 查看是否在叶节点中
        InTree.children[items[0]].inc(count)
    else:
        InTree.children[items[0]] = TreeNode(items[0], count, InTree)
        if headerTable[items[0]][1] is None:  # 更新位置
            headerTable[items[0]][1] = InTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], InTree.children[items[0]])
    # 使用递归
    if len(items) > 1:
        updateTree(items[1:], InTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode): # 更新标记
    while nodeToTest.nodeLink != None: # 如果连接不为空，就继续找
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath): # 递归回溯父节点
    if leafNode.parent != None:# 如果父节点不为空
        prefixPath.append(leafNode.name)# 加入列表
        ascendTree(leafNode.parent, prefixPath)# 回溯


def findPrefixPath(basePat, headTable): # 得到条件模式基
    condPats = {}   # 保存
    treeNode = headTable[basePat][1]
    while treeNode != None:# 树节点不为空
        prefixPath = [] # 记录所有父节点
        ascendTree(treeNode, prefixPath) # 回溯父节点
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup=1, preFix=set([]), freqItemList=[]):
    # 排序，根据出现次数和本身
    temp = list(headerTable.keys())
    bigL = sorted(temp, key=lambda p: (headerTable[p][0],p))

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        # 通过条件模式基找到的频繁项集
        condPattBases = findPrefixPath(basePat, headerTable) # 条件模式基
        myCondTree, myHead = createTree(condPattBases, minSup)# 创建条件FP树
        if myHead != None:
            print('condPattBases: ', basePat, condPattBases)# 打印条件模式基
            myCondTree.print_self() # 打印自身结构
            print('*' * 30)# 分隔符
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList) # 递归


class TreeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue   # 节点名称
        self.count = numOccur   # 计数
        self.nodeLink = None    # 用于连接相似结点
        self.parent = parentNode# 父节点
        self.children = {}      # 子节点

    def inc(self, numOccur):
        self.count += numOccur

    def print_self(self, ind = 1):
        print('   '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.print_self(ind+1)


# 程序开始
items = [['r', 'z', 'h', 'j', 'p'],
         ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
         ['z'],
         ['r', 'x', 'n', 'o', 's'],
         ['y', 'r', 'x', 'z', 'q', 't', 'p'],
         ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]


# 程序开始
tree, headerTable = createTree(items, 3)



# 查找频繁项集

condPats = findPrefixPath('z', headerTable)
print('z', condPats)
condPats = findPrefixPath('x', headerTable)
print('x', condPats)
condPats = findPrefixPath('y', headerTable)
print('y', condPats)
condPats = findPrefixPath('t', headerTable)
print('t', condPats)
condPats = findPrefixPath('s', headerTable)
print('s', condPats)
condPats = findPrefixPath('r', headerTable)
print('r', condPats)

mineTree(tree, headerTable, 2)
