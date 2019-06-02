# LL（1）文法扫描器:
# 根据现有的文法
# 创建first集
# 创建follow集
# 创建预测分析表
# 对输入的字符进行分析
flag = 0

def add_value(dict, key, value): # 列表中添加元素
    global flag
    if key not in dict:
        dict[key] = [value]
        flag = 1
    elif value not in dict[key]:
        dict[key].append(value)
        flag = 1


def add_list(dict, key1, key2): # 列表2的内容给列表1，去重去空符
    global flag
    if key2 not in dict:
        dict[key2] = []
        flag = 1
    if key1 not in dict:
        dict[key1] = []
        flag = 1
    for a in dict[key2]:
        if a not in dict[key1] and a != '^':
            dict[key1].append(a)
            flag = 1


class LL1():
    def __init__(self):
        self.grammer = {}   # 文法
        self.start_V = ''   # 文法的开始符
        self.V_N = []       # 文法的非终结符
        self.V_T = []       # 文法的终结符
        self.V_N_T = []     # 并集
        self.test_input = ''# 样例输入
        self.First = {}     # first集
        self.Follow = {}    # follow集
        self.Table = {}     # 分析表


    def get_grammer(self):
        # 用于得到文法
        '''
        E->TE'
        E'->+TE'|^
        T->FT'
        T'->*FT'|^
        F->(E)|i
        '''

        self.grammer = {
            'E': [['T', '_E']],
            '_E': [['+', '_E'], ['^']],
            'T': [['F', '_T']],
            '_T': [['*', 'F', '_T'], ['^']],
            'F': [['(', 'E', ')'], ['i']],
        }

        self.V_N = ['E', '_E', 'T', '_T', 'F']
        self.V_T = ['+', '*', '(', ')', 'i', '^']
        self.V_N_T = ['E', '_E', 'T', '_T', 'F',
                      '+', '*', '(', ')', 'i', '^']
        self.start_V = 'E'

    def input_data(self):
        self.test_input = 'i+i*i'

    def create_first(self):
        # 默认要处理的都是单个非终结符
        global flag
        while True:
            flag = 0  # 判断First集
            # 对于每一个非终结符
            for key in self.grammer:
                if key in self.V_T: # 终结符
                    add_value(self.First, key, key)
                else:   # 非终结符
                    for part in self.grammer[key]:
                        # 非终结符->终结符开头
                        if part[0] in self.V_T:
                            add_value(self.First, key, part[0])
                        else: # 非终结符->非终结符开头
                            # 把非终结符First集加入原来的First中
                            add_list(self.First, key, part[0])
                            pass

                        # 判断目前是否能够推出空符
                        for i in range(0, len(part)-1):
                            if part[i] not in self.First or '^' not in self.First[part[i]]:
                                break
                            add_list(self.First, key, part[i+1])
                            if i == len(part)-2 and '^' in self.First[part[i+1]]:
                                add_value(self.First, key, '^')



            if flag == 0: # First没有变化，结束
                break


    def create_follow(self):
        pass

    def create_analyse(self):
        pass

    def check(self):
        print(self.First)
        pass






def main():
    LL = LL1()
    LL.get_grammer()
    LL.create_first()
    LL.create_follow()
    LL.create_analyse()
    LL.input_data()
    LL.check()


if __name__ == '__main__':
    main()
