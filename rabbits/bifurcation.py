#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import *
from pylab import *
from scipy import stats

# f(x)
f = lambda x,r : r * x * ( 1 -x )
# набор r
rlist = linspace( 0, 4, 1000)
# начальная популяция зайцев
X = [ 0.3 * ones_like(rlist), ]
# эволюция за N шагов
for i in arange(0,2000):  X += [ f(X[ -1], rlist) , ]
# берём последние N
X = hsplit( vstack(X[-1000:]), rlist.size)
# Разбиваем на участки по вертикали (чем больше точек, тем ярче будет участок)
H = map( lambda Z : stats.histogram( Z, defaultlimits=(0,1), numbins=300 )[0],X)
# нормируем по весу и инвертируем цвет (чтобы линия была чёрной а не белой)
H = map( lambda Z : 1-Z/Z.max(), H )
figure( figsize=(8, 5), dpi=130 )
imshow( rot90(vstack(H)), aspect = 'auto' , extent = [0, 4, 0, 1])
bone() # переводим цвет в чб
xlabel('r')
ylabel(r'$X_{n \rightarrow \infty}$')
savefig('Bifurcation.png')
