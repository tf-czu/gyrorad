#!/usr/bin/python
"""
  Read serial COM port
  usage:
       ./reader.py <com> <speed>
"""
import sys
import serial
import datetime

def reader( com ):
    dt = datetime.datetime.now()
    filename = "g" + dt.strftime("%y%m%d_%H%M%S.log")
    f = open( filename, "wb" )
    while True:
        f.write( com.read(100) )
        f.flush()
        sys.stderr.write('.')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(2)
    reader( com = serial.Serial( sys.argv[1], int(sys.argv[2]) ) )

# vim: expandtab sw=4 ts=4 

