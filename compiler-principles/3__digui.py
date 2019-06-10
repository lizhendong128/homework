# 递归下降法
def test():
    global index
    return test_input[index]


def E():
    T()
    _E()


def _E():
    global index
    if test() == '+':
        index += 1
        T()
        _E()


def T():
    F()
    _T()


def _T():
    global index
    if test() == '*':
        index += 1
        F()
        _T()


def F():
    global index
    if test() == '(':
        index += 1
        E()
        if test() == ')':
            index += 1
    elif test() == 'i':
        index += 1
    else:
        error()


def error():
    print('非法的符号串!')
    exit()



# 程序的开始
print('递归下降分析程序，编制人:李振东，201601060610，计算机2016-4')
print('输入一以#结束的符号串(包括+—*/（）i#)：')
test_input = input()
# test_input = 'i+i*i#'
if test_input[-1] != '#':
    print('ERROR! 结尾一定要是#')
    exit()

index = 0
E()
if test() != '#':
    error()
else:
    print('输出结果：' + test_input + '为合法符号串')



















