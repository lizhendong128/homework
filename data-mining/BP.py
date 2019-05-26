import math
import random

random.seed(0)


def rand(a, b): # 生成a,b之间的随机数
    return (b - a) * random.random() + a


def make_matrix(m, n, fill=0.0): # 创造一个指定大小的矩阵
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x): # Sigmoid函数,阈值函数
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x): # sigmod的导数
    return x * (1 - x)


class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0 # 输入的维度
        self.hidden_n = 0 # 隐含层神经元个数
        self.output_n = 0 # 输出层个数
        self.input_cells = [] # 存储输入的内容
        self.hidden_cells = [] # 隐藏层的输出
        self.output_cells = [] # 输出层的输出
        self.input_weights = [] # 输入权重
        self.output_weights = [] # 输出权重
        self.input_correction = []
        self.output_correction = []

    # 初始化神经网络
    def setup(self, ni, nh, no):
        self.input_n = ni + 1 # 初始化输入维度
        self.hidden_n = nh # 初始化隐藏层个数
        self.output_n = no # 初始化输出层个数
        # 初始化神经元
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # 初始化权重矩阵
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        # 取任意值
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2) # (-0.2, 0.2)的任意数
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0) # (-2.0, 2.0)的任意数
        # 初始化 correction 矩阵
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    # 进行一次前馈， 并返回输出
    def predict(self, inputs):
        # 激活输入层
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i] # 保存输入内容
        # 激活隐藏层
        for j in range(self.hidden_n): # 对于每一个隐藏层
            total = 0.0 # 输入*权重的之和
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total) # 保存隐藏层的输出
        # 激活输出层
        for k in range(self.output_n): # 对于每一个输出层
            total = 0.0 # 输入*权重的之和
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total) # 保存输出层的输出
        return self.output_cells[:] # 返回输出层

    # 定义一次反向传播和更新权值的过程， 并返回最终预测误差
    def back_propagate(self, case, label, learn, correct):
        # 前馈
        self.predict(case)
        # 得到输出层的误差
        output_deltas = [0.0] * self.output_n # 初始化输出层误差矩阵
        for o in range(self.output_n): # 对于每一个输出
            error = label[o] - self.output_cells[o] # 计算差值
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error # 得到误差
        # 得到隐藏层的误差
        hidden_deltas = [0.0] * self.hidden_n # 初始化隐藏层误差矩阵
        for h in range(self.hidden_n): # 对于每一个隐藏层
            error = 0.0 # 误差初值
            for o in range(self.output_n): # 对于每一个输出层
                error += output_deltas[o] * self.output_weights[h][o] # 下一层单元的误差加权和
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error # 计算误差
        # 更新输出权重
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # 更新输入权重
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # 得到全局误差
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error # 返回误差

    # 控制迭代， 该方法可以修改最大迭代次数， 学习率λ， 矫正率μ三个参数
    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for j in range(limit): # 对于每一次迭代
            error = 0.0
            for i in range(len(cases)): # 对于样例中的每一个
                label = labels[i] #赋值
                case = cases[i] # 赋值
                error += self.back_propagate(case, label, learn, correct) # 训练，计算误差

    # 使用神经网络学习 异或逻辑
    def test(self):
        cases = [ # 样例
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
        ]
        labels = [[0], [1], [1], [0]] # 目标
        self.setup(2, 5, 1) # 初始化
        self.train(cases, labels, 10000, 0.05, 0.1) # 训练
        for case in cases: # 进行预测
            print(self.predict(case)) # 输出预测值


if __name__ == '__main__':
    nn = BPNeuralNetwork() # 创建对象
    nn.test() # BP神经网络算法启动
