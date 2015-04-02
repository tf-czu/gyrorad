from splitter import *
import unittest


class SplitterTest( unittest.TestCase ): 
    def testStripFirstLine( self ):
        data = """\x1c\xfc\x00\xe0\xe0\x1c\xe0\x1c\x1c\x1c\x1c\xe0\xfc\x1c\xfc\xe0\xe0b\xfa
        
id,timeMs,accX,accY,accZ,temp,gyroX,gyroY,gyroZ
0,82,-14484,7784,-2500,27.68,-101,131,-55
1,89,15648,6576,-552,27.07,202,211,-245
2,100,-13024,9196,-1188,26.55,-225,-129,-172
3"""
        self.assertTrue( stripHeader( data ).startswith("0,82,-14484,7784,"), data )


    def testGrepGyro0( self ):
        data = """0,82,-14484,7784,-2500,27.68,-101,131,-55
1,89,15648,6576,-552,27.07,202,211,-245
"""
        self.assertEqual( splitter(data, "0"), "0,82,-14484,7784,-2500,27.68,-101,131,-55\n" )

        data = """
0,82,-14484,7784,-2500,27.68,-101,131,-55
1,89,15648,6576,-552,27.07,202,211,-245
2,100,-13024,9196,-1188,26.55,-225,-129,-172
3,112,17256,1472,-1744,28.01,-116,-74,503
0,122,-14480,7792,-2436,27.68,-113,128,22
1,134,15688,6432,-484,27.17,243,131,37
2,145,-12980,9284,-1068,26.51,-216,-146,-144
3,156,17240,1488,-1736,28.06,-66,-165,-561
0,167,-14460,7768,-2404,27.64,-137,116,38
1,179,15564,6568,-464,27.26,209,146,-58
2,190,-12948,9336,-1140,26.60,-221,-137,-181
3,201,17244,1448,-1700,28.11,-111,-118,218
0,214,-14516,7792,-2500,27.59,-110,162,72
1,224,15664,6448,-372,27.21,228,225,-316"""
        self.assertEqual( len(splitter(data, "0").split('\n')), 4+1 ) # counts last empty string


if __name__ == "__main__":
    unittest.main() 
# vim: expandtab sw=4 ts=4 

