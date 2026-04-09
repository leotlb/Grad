import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

def fun_poli1(t,a,b):
     return a+(b*t)

def fun_poli6(t, a0, a1, a2, a3, a4, a5, a6):
     return (a0 + (a1 * pow(t, 1)) + (a2 * pow(t, 2)) + (a3 * pow(t, 3)) + (a4 * pow(t, 4)) + (a5 * pow(t, 5))
             + (a6 * pow(t, 6)) )

def fun_trigo1(t,a0,a1,b1):
     return (a0 + a1 * np.cos(t) + b1 * np.sin(t))

def fun_trigo29(t, a0, a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, a6, b6, a7, b7, a8, b8, a9, b9, a10, b10, a11, b11, a12,
              b12, a13, b13, a14, b14, a15, b15, a16, b16, a17, b17, a18, b18, a19, b19, a20, b20, a21, b21, a22, b22,
              a23, b23, a24, b24, a25, b25, a26, b26, a27, b27, a28, b28, a29, b29):
     return (a0 + a1*np.cos(t) + b1*np.sin(t) + a2*np.cos(2*t) + b2*np.sin(2*t) + a3*np.cos(3*t) + b3*np.sin(3*t)
             + a4*np.cos(4*t) + b4*np.sin(4*t) + a5*np.cos(5*t) + b5*np.sin(5*t) + a6*np.cos(6*t) + b6*np.sin(6*t)
             + a7*np.cos(7*t) + b7*np.sin(7*t) + a8*np.cos(8*t) + b8*np.sin(8*t) + a9*np.cos(9*t) + b9*np.sin(9*t)
             + a10*np.cos(10*t) + b10*np.sin(10*t) + a11*np.cos(11*t) + b11*np.sin(11*t) + a12*np.cos(12*t) + b12*np.sin(12*t)
             + a13*np.cos(13*t) + b13*np.sin(13*t) + a14*np.cos(14*t) + b14*np.sin(14*t) + a15*np.cos(15*t) + b15*np.sin(15*t)
             + a16*np.cos(16*t) + b16*np.sin(16*t) + a17*np.cos(17*t) + b17*np.sin(17*t) + a18*np.cos(18*t) + b18*np.sin(18*t)
             + a19*np.cos(19*t) + b19*np.sin(19*t) + a20*np.cos(20*t) + b20*np.sin(20*t) + a21*np.cos(21*t) + b21*np.sin(21*t)
             + a22*np.cos(22*t) + b22*np.sin(22*t) + a23*np.cos(23*t) + b23*np.sin(23*t) + a24*np.cos(24*t) + b24*np.sin(24*t)
             + a25*np.cos(25*t) + b25*np.sin(25*t) + a26*np.cos(26*t) + b26*np.sin(26*t) + a27*np.cos(27*t) + b27*np.sin(27*t)
             + a28*np.cos(28*t) + b28*np.sin(28*t) + a29*np.cos(29*t) + b29*np.sin(29*t))


y = [202.2, 94.9, 89.1, 24.8, 29.7, 52, 65.2, 24, 0.5, 1.3, 15.1, 2.2, 28.6, 174.3,
     65.6, 24.7, 25.5, 7.8, 4.9, 0, 1.8, 0, 0.7, 207.8, 133.8, 187.6, 127.9, 131,
     28, 4.2, 0.2, 0, 0, 1, 38.4, 68.5, 44.3, 109.8, 114.9, 101.7, 65, 8.4, 15.8,
     0, 0, 0, 5.1, 409.2, 243.9, 98.3, 51.7, 81.1, 81.5, 20.4, 1.5, 4.1, 0, 0.5, 26, 73.4]
x = np.arange(1, 61, 1)

y_mean = np.mean(y)

final = []
(final), _ = opt.curve_fit(fun_poli6, x, y)
print('estimativa dos indices')
print(final)

y_est = fun_poli6(x, *final)

plt.plot(x, y, 'o')
plt.plot(x, y_est, '-')
plt.show()

sqt = 0.0
sqr = 0.0
i = 0
for i in range (0,len(final),1):
     sqt += (y[i]-y_mean)**2
     sqr += (fun_poli6(i, *final) - y[i])**2

deter = (sqt-sqr)/sqt
print('estimativa de 72 meses')
print(fun_poli6(72, *final))
print('coeficiente de determinação')
print(deter)


###################################################
# def fun_trigo(t, *ind):
#     soma = ind[0]
#     it = 1
#     for i in range (1,len(ind),2):
#         soma += ind[i]*np.cos(it*t) + ind[i+1]*np.sin(it*t)
#         it += 1
#     return sum
#
# inicio = np.random.randn(len(y)-1)
# print(inicio)
#
# final = []
# (final), _ = opt.curve_fit(fun_trigo, x, y, p0=inicio)
# y_est = fun_trigo(x, *final)
#
# plt.plot(x, y, 'o')
# plt.plot(x, y_est, '-')
# plt.show()


