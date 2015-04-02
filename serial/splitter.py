#!/usr/bin/python
"""
  Split logged data into separate "channels"
  usage:
       ./splitter.py <log file> <GPS|0..3>
"""
import sys

FIRST_LINE = "id,timeMs,accX,accY,accZ,temp,gyroX,gyroY,gyroZ\n"

def stripHeader( data ):
    if FIRST_LINE in data:
        return data[ data.find(FIRST_LINE) + len(FIRST_LINE): ]
    return data

def splitter( data, selected ):
    assert selected in ['GPS','0','1','2','3'], selected
    data = stripHeader( data )
    result = ""
    for line in data.split('\n'):
        if line.startswith( selected ):
            result += line + '\n'
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(2)
    print splitter( open(sys.argv[1], "rb").read(), selected=sys.argv[2] )

# vim: expandtab sw=4 ts=4 

