#!/usr/bin/python
"""
  Plot CSV data
  usage:
       ./plot.py <csv data>
"""
import sys
import matplotlib.pyplot as plt


def getArray( filename ):
    prev = None
    arr = []
    for line in open(filename):
        try:
            v = [float(x) for x in line.split(',')]
            if prev:
                arr.append( v[1] - prev[1] )
            prev = v
        except ValueError as e:
            print e, line
    return arr

def draw( arr ):
    plt.plot(arr, 'o-', linewidth=2)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(2)
    draw( getArray(sys.argv[1]) )

# vim: expandtab sw=4 ts=4 

