# 参考C语言代码 ： https://www.cnblogs.com/zyrblog/p/6885922.html
import re
import copy

class Scanner(object):
    # 保留字 -- 1
    reserveWord = [
        "auto", "break", "case", "char", "const", "continue",
        "default", "do", "double", "else", "enum", "extern",
        "float", "for", "goto", "if", "int", "long",
        "register", "return", "short", "signed", "sizeof", "static",
        "struct", "switch", "typedef", "union", "unsigned", "void",
        "volatile", "while"
    ]

    # 标识符 -- 2
    # 无符号整形数 -- 3

    # 运算符 -- 4
    operator = [
        "+", "-", "*", "/", "<", "<=", ">", ">=", "=", "==",
        "!=","&","&&","|","||","%","<<",">>","+="
    ]

    # 分隔符 -- 5
    Delimiter = [
        ";", "(", ")", "^", ",", "\"", "\'","[","]","{","}"
    ]

    # 错误符 -- 6

# ------------------------------------------------------------------------------------------------------------- #

    # 判断是否为保留字 -- 1
    def searchReserve(self, reserveWord):
        if reserveWord in self.reserveWord:
            return True
        else:
            return False # 表示不是保留字，是标识符
        pass

    # 判断是否为字母
    def IsLetter(self, letter):
        if re.match(r'[a-zA-Z\_]', letter): # 正则表达式
            return True
        else:
            return False

    # 判断是否为数字
    def IsDigit(self, digit):
        if re.match(r'\d', digit):
            return True
        else:
            return False
        pass

    # 判断是否为运算符或者分隔符
    def IsSign(self, Sign):
        if Sign in self.Delimiter:
            return 5
        elif Sign in self.operator:
            return 4
        else:
            return -1

    # 过滤器，过滤掉注释
    def filterResource(self, code):
        note = 0
        code_temp=[]
        for line in range(len(code)):
            a = ''
            s_line = code[line]
            i = -1
            while i < len(s_line)-1:
                i = i + 1
                if i<=len(s_line)-2 and s_line[i]=='/' and s_line[i+1]=='/' and note == 0:
                    break    # 跳过单行注释

                if i<=len(s_line)-2 and s_line[i]=='/' and s_line[i+1]=='*':
                    note = 1
                    continue   # 注释开始

                if i<=len(s_line)-2 and s_line[i]=='*' and s_line[i+1]=='/':
                    note = 0
                    i = i + 2
                    continue # 注释结束

                if note == 0 and s_line[i]!='\t' and s_line[i]!='\n' and s_line[i]!='\v' and s_line[i]!='\r':
                    a = a + s_line[i]

            # print(a)
            if a != '':
                code_temp.append(a)

        code = copy.deepcopy(code_temp)

        return code


def clear_number(number_list):
    number_list[0] = number_list[1] = 0
    pass

def clear_sign(sign_list):
    sign_list[0] = ''
    sign_list[1] = 0

def clear_word(word):
    word = ''

# 主程序
# 读取文件
scanner = Scanner()
code = []
with open('D:/test.txt', 'r',encoding='UTF-8') as f:
    for line in f.readlines():
        code.append(line.strip())

    # 代码过滤
    code = scanner.filterResource(code)
    # print(code)

    # 代码识别：
    # 字符分为符号和非符号，非符号之间用空格隔开，符号和非符号之间不需要隔开
    # 利用空格或者符号进行识别
    for line in code:
        word = ''
        number = 0
        number_e = 0

        sign = ''
        sign_e = 0
        number_list = [number, number_e]
        sign_list = [sign, sign_e]

        number_or_word = 0
        number_plus = 1

        i = -1
        while i < len(line)-1:
            i=i+1
            bit = line[i]
            number_or_word = 0

            # (识别符号)符号打头，顺便去除符号-前面-的字母或者数字
            if scanner.IsSign(bit) > 0 and sign_list[1] > 0 and scanner.IsSign(sign_list[0]+bit) < 0:
                # 如果两个连续的符号不是符号，输出第一个符号，继续
                print('(', sign_list[1], ',"', sign_list[0], '")')
                clear_sign(sign_list)

            if scanner.IsSign(bit) > 0: # 把符号保存
                sign_list[0] = sign_list[0] + bit
                sign_list[1] = scanner.IsSign(bit)
            if scanner.IsSign(bit) > 0 and word != '':
                # 字母+符号，输出字母
                if scanner.searchReserve(word) == True:
                    print('(', 1, ',"', word, '")')
                else:
                    print('(', 2, ',"', word, '")')
                word = ''
                number_or_word=0
                # number_plus = 1
            elif scanner.IsSign(bit) > 0 and number_list[1] != 0:
                # 数字+符号，输出数字
                print('(', 3, ',"', number_plus*number_list[0], '")')
                clear_number(number_list)
                number_or_word = 0
                number_plus = 1


            #字母打头（识别单词）
            if scanner.IsLetter(bit) and sign_list[1] > 0:
                # 符号 + 字母，识别符号，继续字母
                print('(', sign_list[1], ',"', sign_list[0], '")')
                clear_sign(sign_list)


            if scanner.IsLetter(bit) and number_list[1]==0:   # 遇见字母
                word = word + bit
                number_or_word = 1    # 标识前一个字符是单词
                continue
            elif word != '' and scanner.IsDigit(bit): #字母加数字
                word = word + str(bit)
                continue
            elif word != '' and bit == ' ': # 字母加空格
                if scanner.searchReserve(word) == True:
                    print('(', 1, ',"', word, '")')
                else:
                    print('(', 2, ',"', word, '")')
                word = ''
                continue


            # 数字打头（识别数字）
            if scanner.IsDigit(bit)==True and sign_list[1] > 0:
                # 符号 + 数字，识别符号，继续数字
                # 在这里识别正负号！！
                if sign_list[0] not in ['+', '-']:  # 如果符号不是正负号
                    print('(', sign_list[1], ',"', sign_list[0], '")')
                    clear_sign(sign_list)
                elif number_or_word > 0:# 如果前面存在数字或者单词，那么这个符号就是运算符
                    pass
                elif number_or_word == 0:#符号是正负号，纳入数字
                    number_plus = int(sign_list[0]+'1 ')
                    clear_sign(sign_list)
                # number_or_word = 1

            if scanner.IsDigit(bit)==True and word == '':  # 数字打头
                number_list[1] = 1
                number_list[0] = number_list[0] * 10 + int(bit)
                number_or_word = 1  # 标识前一个字符是数字
            elif number_list[1] == 1 and scanner.IsLetter(bit):
                # 说明是数字 + 字母 ，是错误的
                print('Error : (', 6, ',"', str(number_list[0]) + bit, '")')
                clear_number(number_list)
                clear_sign(sign_list)
                word = ''
            elif number_list[1] == 1 and bit == ' ':
                # 遇到空格,数字识别成功，输出数字
                print('(', 3, ',"', number_plus*number_list[0], '")')
                number_plus = 1
                clear_number(number_list)

            if bit == ' ' and sign_list[1] != 0:
                # 符号加空格，输出符号，清空标志，继续
                print('(', sign_list[1], ',"', sign_list[0], '")')
                clear_sign(sign_list)
            if i == len(line) - 1:
                print('(', sign_list[1], ',"', sign_list[0], '")')
