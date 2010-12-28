#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import *
from pylab import *
from scipy import stats
from scipy import fftpack

N = 2048

# f(x)
f = lambda x,r : r * x * ( 1 -x )
# набор r
rlist = linspace( 2.99, 3.99, 20)
# начальная популяция зайцев
X = [ 0.2 * ones_like(rlist), ]
# эволюция за N шагов
for i in arange(0,N+1000):  X += [ f(X[ -1], rlist) , ]

X = hsplit( vstack(X[-N:]), rlist.size)

def fourier(Z):
    Z = hstack(Z)
    Z = fft(Z)
    Z = abs(Z[1:len(Z)/2])#**2
    return Z

F = map ( fourier, X)

figure( figsize=(8, 5), dpi=130 )
for i in range(len(rlist)):
    filename = str('%04d' % i) + '.png'
    print filename
    title('r = %.3f' % rlist[i])
    xlabel('Normalized frequency')
    ylabel('Amplitude spectrum')
    fn = np.linspace(0.0,1.0, len(F[i]))
    plot(fn, F[i])
    ylim([0,100])
    plt.savefig(filename, dpi=100)
    clf() # clear figure
