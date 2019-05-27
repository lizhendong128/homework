# 自己用Python实现了金刚石绘制功能
# 无奈窗口界面几乎无法实现
# 所以最后还是用vs

import numpy as np
import matplotlib.pyplot as plt
from pylab import *

R = 300 # 半径
number_point =  30 #等分点数量

figure(figsize=(8,8), dpi=80)
temp = np.linspace(0, 2*np.pi, 1000)
X = np.sin(temp)*R
Y = np.cos(temp)*R
plot(X,Y,linewidth=1.0,linestyle=':')

x=[]
y=[]
for i in range(number_point):
  x.append(R*np.sin(i*2*pi/number_point))
  y.append(R*np.cos(i*2*pi/number_point))

for i in range(number_point):
  for j in range(number_point):
    if(i!=j):
      plt.plot([x[i],x[j]],[y[i],y[j]])

show()
