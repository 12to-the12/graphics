import numpy as np

x = np.array([1,0,0])
y = np.array([0,1,0])
z = np.array([0,0,1])
a = np.array([1,0,1])
b = np.array([0.5,0,0.5])
c = np.array([-0.5,0,0])
c = np.array([-0.5,0,0.5])
d = np.array([-1,0,0])
print(np.dot(x,a))
print(np.dot(x,b))
print(np.dot(x,c))
print(np.dot(x,d))