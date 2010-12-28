#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import *
from pylab import *
from scipy import stats

# f(x)
f = lambda x,r : r * x * ( 1 -x )
# набор r
rlist = linspace( 3.5, 3.7, 500)
# начальная популяция зайцев
X = [ 0.3 * ones_like(rlist), ]
# эволюция за N шагов
for i in arange(0,5000):  X += [ f(X[ -1], rlist) , ]
# берём последние N
X = hsplit( vstack(X[-2000:]), rlist.size)
# Разбиваем на участки по вертикали (чем больше точек, тем ярче будет участок)
H = map( lambda Z : stats.histogram( Z, defaultlimits=(0.3,0.7), numbins=500 )[0],X)
# нормируем по весу и инвертируем цвет (чтобы линия была чёрной а не белой)
H = map( lambda Z : 1-sqrt(Z/Z.max()), H )
scale = 1
figure( figsize=(8*scale, 5*scale), dpi=130 )
imshow( rot90(vstack(H)), aspect = 'auto' , extent = [3.5, 3.7, 0.3, 0.7])
bone() # переводим цвет в чб
xlabel('r')
ylabel(r'$X_{n \rightarrow \infty}$')
savefig('Small_bifurcation.png')
