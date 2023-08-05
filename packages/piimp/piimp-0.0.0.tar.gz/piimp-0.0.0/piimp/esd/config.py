import os, sys, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

def read_file(file):
    f=open(file, 'r')
    r=f.readlines()
    f.close()
    return r

def plot_MS_profile(csvfile):
    data = read_file(csvfile)
    x    = 'mass amu'
    y    = 'SEM c/s'

    for line in data:
        if '"Time","ms",' in line:
            i = data.index(line)
            break

    df = pd.read_csv(csvfile, header=i)

    df.plot(x,y, legend=False)
    plt.ylabel('Ion Signal (c/s)')
    plt.xlabel('Mass (amu)')
    plt.gca().xaxis.set_major_locator(MultipleLocator(20))
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(10))
    plt.xlim(-9, 209)
    plt.show()

    return
