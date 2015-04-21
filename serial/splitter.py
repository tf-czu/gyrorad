#!/usr/bin/python
"""
  Split logged data into separate "channels"
  usage:
       ./splitter.py <log file> <GPS|0..3>
"""
import sys

FIRST_LINE = "id,timeMs,accX,accY,accZ,temp,gyroX,gyroY,gyroZ\n"

GPS_SEPARATOR_BEGIN = chr(0x2)
GPS_SEPARATOR_END   = chr(0x3)

def stripHeader( data ):
    if FIRST_LINE in data:
        return data[ data.find(FIRST_LINE) + len(FIRST_LINE): ]
    return data

def splitter( data, selected ):
    assert selected in ['GPS','0','1','2','3'], selected
    selectedGPS = selected == 'GPS'
    gpsSection = False
    data = stripHeader( data )
    result = ""
    for line in data.split('\n'):
        if selectedGPS:
            if GPS_SEPARATOR_BEGIN in line:
                if GPS_SEPARATOR_END in line:
                    result += line.split(GPS_SEPARATOR_BEGIN)[1].split(GPS_SEPARATOR_END)[0]
                    gpsSection = False
                else:
                    result += line.split(GPS_SEPARATOR_BEGIN)[1]
                    gpsSection = True
            elif GPS_SEPARATOR_END in line:
                result += line.split(GPS_SEPARATOR_END)[0]
                gpsSection = False
            elif gpsSection:
                result += line.strip() + '\n'
            
        if len(line.split(',')) >= 9:
            if line[:2] not in ['0,','1,','2,','3,']:
                parts = line.split(',')
                s = parts[-9]
                if len(s) > 0:
                    line = parts[-9][-1] + ',' + ",".join( parts[-8:] )
            if line.startswith( selected ) and '*' not in line:
                result += line.strip() + '\n'
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(2)
    print splitter( open(sys.argv[1], "rb").read(), selected=sys.argv[2].upper() )

# vim: expandtab sw=4 ts=4 

