import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

numdays=10
x=2
base = datetime.datetime.today()
date_list = {base - datetime.timedelta(seconds=x):np.random.random() for x in range(numdays)}
print (date_list)

lists = sorted(date_list.items()) 
x, y = zip(*lists)

plt.ion()
for i in range(100):
    x = range(i)
    y = range(i)
    # plt.gca().cla() # optionally clear axes
    plt.plot(x, y)
    plt.title(str(i))
    plt.draw()
    plt.pause(0.1)

plt.show(block=True)
print("-----------------------------")