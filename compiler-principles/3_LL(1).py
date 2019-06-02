# LL（1）文法扫描器:
# 根据现有的文法
# 创建first集
# 创建follow集
# 创建预测分析表
# 对输入的字符进行分析

t_special_word = r'\+|-|\*|/|\(|\)|:|\'|=|\[|\]|,'

class LL1():
    def __init__(self):
        self.grammer = {}   # 文法
        self.start_V = ''   # 文法的开始符
        self.V_N = []       # 文法的非终结符
        self.V_T = []       # 文法的终结符
        self.V_N_T = []     # 并集
        self.test_input = ''# 样例输入
        self.Fisrt = {}     # first集
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
            'T': [['F'], ['_T']],
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
        for key in self.grammer.keys():





        pass

    def create_follow(self):
        pass

    def create_analyse(self):
        pass

    def check(self):
        pass






def main():
    LL = LL1()
    LL1.get_grammer()
    LL.create_first()
    LL.create_follow()
    LL.create_analyse()
    LL.input_data()
    LL.check()


if __name__ == '__main__':
    main()
