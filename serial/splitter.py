#!/usr/bin/python
"""
  Split logged data into separate "channels"
  usage:
       ./splitter.py <log file> <GPS|0..3|all>
"""
import sys

FIRST_LINE = "id,timeMs,accX,accY,accZ,temp,gyroX,gyroY,gyroZ\n"

GPS_SEPARATOR_BEGIN = chr(0x2)
GPS_SEPARATOR_END   = chr(0x3)


def checksum( s ):
    sum = 0
    for ch in s:
        sum ^= ord(ch)
    return "%02X" % (sum)

def ddmm2ddd( s ):
    num,frac = ('0000' + s).split('.')
    d = float(num[-2:]+'.'+frac)/60.0 + float(num[-4:-2]) 
    return d

def parseNMEA( data ):
    ret = []
    for line in data.replace('\r','\n').split('\n'):
        if '$' in line and '*' in line.split('$')[-1]:
            s = line.split('$')[-1].split('*')
            if len(s) > 1 and len(s[1]) >= 2:
                if checksum(s[0]) == s[1][:2]:
                    if s[0].startswith("GPRMC"):
                        s = s[0].split(',')[:7]
                        if len(s) >= 7 and s[2] == 'A' and s[4] == 'N' and s[6] == 'E':
                            ret.append( (s[1], ddmm2ddd(s[3]), ddmm2ddd(s[5])) )
                    elif s[0].startswith("GPGGA"):
                        s = s[0].split(',')[:6]
                        if len(s) >= 6 and s[3] == 'N' and s[5] == 'E':
                            ret.append( (s[1], ddmm2ddd(s[2]), ddmm2ddd(s[4])) )
    return ret


def stripHeader( data ):
    if FIRST_LINE in data:
        return data[ data.find(FIRST_LINE) + len(FIRST_LINE): ]
    return data

def splitter( data, selected ):
    assert selected in ['GPS','0','1','2','3','ALL'], selected
    gpsSection = False
    data = stripHeader( data )
    result, resultGPS = "", ""
    lastGPS = None
    records = []
    lastSeek = 0
    for line in data.split('\n'):
        if GPS_SEPARATOR_BEGIN in line:
            if GPS_SEPARATOR_END in line:
                resultGPS += line.split(GPS_SEPARATOR_BEGIN)[1].split(GPS_SEPARATOR_END)[0]
                line = line.split(GPS_SEPARATOR_BEGIN)[0] + line.split(GPS_SEPARATOR_END)[1]
                gpsSection = False
            else:
                resultGPS += line.split(GPS_SEPARATOR_BEGIN)[1]
                line = line.split(GPS_SEPARATOR_BEGIN)[0]
                gpsSection = True
        elif GPS_SEPARATOR_END in line:
            resultGPS += line.split(GPS_SEPARATOR_END)[0]
            line = line.split(GPS_SEPARATOR_END)[1]
            gpsSection = False
        elif gpsSection:
            resultGPS += line.strip() + '\n'
            line = ""
            
        arr = parseNMEA( resultGPS[lastSeek:] )
        if len(arr) > 0 and arr[-1] != lastGPS:
            lastSeek = max(0, len(resultGPS)-80) # max NMEA line is 80 characters
            lastGPS = arr[-1]
            records.append( lastGPS )

        if len(line.split(',')) >= 9:
            if line[:2] not in ['0,','1,','2,','3,']:
                parts = line.split(',')
                s = parts[-9]
                if len(s) > 0:
                    line = parts[-9][-1] + ',' + ",".join( parts[-8:] )
            if line.startswith( selected ) and '*' not in line:
                result += line.strip() + '\n'
            records.append( [int(x) for x in line.split(',') if '.' not in x] ) # ignore float temperature
    if selected == 'GPS':
        return resultGPS
    if selected == 'ALL':
        return records
    return result




if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(2)
    selected = sys.argv[2].upper()
    data = splitter( open(sys.argv[1], "rb").read(), selected=selected )
    if selected == "GPS":
        print data
        print "------------------"
        print parseNMEA( data )
    elif selected == "ALL":
        for row in data:
            print row
    else:
        print data

# vim: expandtab sw=4 ts=4 

