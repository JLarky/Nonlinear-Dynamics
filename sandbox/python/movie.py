#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Josh Lifton 2004
#
# Permission is hereby granted to use and abuse this document
# so long as proper attribution is given.
#

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt   # For plotting graphs.
import numpy as np
import subprocess                 # For issuing commands to the OS.
import os
import sys                        # For determining the Python version.

import random
from numpy.random import uniform, seed
from matplotlib.mlab import griddata

#
# Print the version information for the machine, OS,
# Python interpreter, and matplotlib.  The version of
# Mencoder is printed when it is called.
#
print 'Executing on', os.uname()
print 'Python version', sys.version
print 'matplotlib version', matplotlib.__version__

try:
    subprocess.check_call(['mencoder'])
except subprocess.CalledProcessError:
    print "mencoder command was found"
    pass # mencoder is found, but returns non-zero exit as expected
    # This is a quick and dirty check; it leaves some spurious output
    # for the user to puzzle over.
except OSError:
    print "The mencoder command was not found"
    sys.exit("quitting\n")


print 'Initializing data set...'   # Let the user know what's happening.

# Initialize variables needed to create and store the example data set.
numberOfTimeSteps = 100   # Number of frames we want in the movie.
numberOfTimeSteps = 10000
numberOfTimeSteps = 1000

# Размер поля
f_m = 30

FPS = 15
make_images = True
make_video = True
make_plots = False
random_drops = False
plot_hist = True

random_drops = make_plots = True
plot_hist = make_video = make_images = False

#hist
FPS = 15; f_m = 5
make_plots = plot_hist = random_drops = make_video = make_images = True

# outs
f_m = 30;make_video = make_images = False;numberOfTimeSteps = 10000

x = np.arange(-10,10,0.01)   # Values to be plotted on the x-axis.

# Поле
field = np.zeros((f_m,f_m), float)

events = np.array([-1.0]*numberOfTimeSteps)
events_sum = np.zeros(numberOfTimeSteps, float)
summ = 0
bins=np.arange(1,50,1)

for i in range(numberOfTimeSteps) :
    if random_drops:
        ek = random.randrange(f_m)
        el = random.randrange(f_m)
    else:
        el = ek = f_m/2
    field[ek,el] += 1 # новая песчинка упала
    acc_event = 0
    while True:
        new_event = 0
        # проверяем не случилось ли лавины
        for k in range(f_m):
            for l in range(f_m):
                if field[k,l] > 4:
                    field[k,l] -= 4
                    try: field[k+1,l] += 1
                    except IndexError: pass
                    try: field[k-1,l] += 1
                    except IndexError: pass
                    try: field[k,l+1] += 1
                    except IndexError: pass
                    try: field[k,l-1] += 1
                    except IndexError: pass
                    new_event += 1
        acc_event += new_event
        # если лавин не было, то можно выходить
        if new_event==0:
            break
    summ += acc_event
    events[i] = acc_event
    events_sum[i] = summ
    if make_images: # отрисовываем новое состояние

        if plot_hist:
            plt.hist(events, bins=bins)
        else:
            plt.imshow(field,vmin=0,vmax=4)
            plt.colorbar()

        plt.title('sandbox (%d steps)' % (i+1))


        filename = str('%04d' % i) + '.png'
        plt.savefig(filename, dpi=100)
        print 'Wrote file', filename
        # Clear the figure to make way for the next image.
        plt.clf()
    else:
        print 'Step %04d' % i

print events

def plot(n, f, filename):
    x = np.arange(0, n, 1)
    y = np.resize(events_sum,n)
    plt.figure(figsize=(8,5), dpi=300)
    f(x,y)
    plt.show()
    plt.savefig(filename)
    plt.clf()

if make_plots:
    plot(1000,  plt.plot,    "out_1k.png")
    plot(3000,  plt.plot,    "out_3k.png")
    plot(3000,  plt.semilogy,"out_3kl.png")
    plot(3000,  plt.loglog,  "out_3kll.png")
    plot(10000, plt.plot,    "out_10k.png")
    plot(10000, plt.semilogy,"out_10kl.png")
    plot(10000, plt.loglog,  "out_10kll.png")

command = ('mencoder',
           'mf://[0-9]*.png',
           '-mf',
           'type=png:w=800:h=600:fps=%s' % FPS,
           '-ovc',
           'lavc',
           '-lavcopts',
           'vcodec=mpeg4',
           '-oac',
           'copy',
           '-o',
           'output.avi')

if make_video:
    print "\n\nabout to execute:\n%s\n\n" % ' '.join(command)
    subprocess.check_call(command)

    print "\n\n The movie was written to 'output.avi'"

    print "\n\n You may want to delete *.png now.\n\n"
else:
    print 'Done'

