#include <BMSerial.h>
#include<Wire.h>

const unsigned char gyroSelectPins[] = { 7, 6, 5, 4 };
const unsigned int NUM_GYROS = sizeof(gyroSelectPins)/sizeof(unsigned char); 

#define GPS_SEPARATOR_BEGIN 0x2
#define GPS_SEPARATOR_END   0x3

class GPSSerial : public BMSerial
{
public:
  GPSSerial() : BMSerial(2,3)
  {
    begin( 9600 );
  }

  void process()
  {
    int b;
    b = read(); 
    while( b >= 0 )
    {
      Serial.write( b ); 
      b = read(); 
    }
  }  
};
GPSSerial gps;

//**************************************************************

//const int MPU=0x68;  // I2C address of the MPU-6050
const int MPU=0x69;  // I2C address of the MPU-6050 for AD0=1
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
long time;

void setup()
{
  int i;
  for( i = 0; i < NUM_GYROS; i++ )
  {
    pinMode( gyroSelectPins[i], OUTPUT ); 
    digitalWrite( gyroSelectPins[i], 0 ); 
  }
    
  Wire.begin();
  for( i = 0; i < NUM_GYROS; i++ )
  {
    digitalWrite( gyroSelectPins[i], 1 );  // select i-th gyro
    delay(10);
    Wire.beginTransmission(MPU);
    Wire.write(0x6B);  // PWR_MGMT_1 register
    Wire.write(0);     // set to zero (wakes up the MPU-6050)
    Wire.endTransmission(true);
    digitalWrite( gyroSelectPins[i], 0 ); // unselect
    delay(10);
  }
  
  
  Serial.begin( 38400 );
  Serial.print( "\n\nid,timeMs,accX,accY,accZ,temp,gyroX,gyroY,gyroZ\n" );
}

void readIthGyro( int i )
{
  digitalWrite( gyroSelectPins[i], 1 );  // select i-th gyro
  delay(1);
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  time = millis();
  Wire.requestFrom(MPU,14,true);  // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  digitalWrite( gyroSelectPins[i], 0 ); // unselect
  delay(1);
}

void loop()
{
  int i;
  for( i = 0; i < NUM_GYROS; i++ )
  {
    readIthGyro( i );
    Serial.print( i );
    Serial.print(","); Serial.print(time);
    Serial.print(","); Serial.print(AcX);
    Serial.print(","); Serial.print(AcY);
    Serial.print(","); Serial.print(AcZ);
    Serial.print(","); Serial.print(Tmp/340.00+36.53);  //equation for temperature in degrees C from datasheet
    Serial.print(","); Serial.print(GyX);
    Serial.print(","); Serial.print(GyY);
    Serial.print(","); Serial.println(GyZ);
  }
  Serial.write( GPS_SEPARATOR_BEGIN );
  gps.process();
  Serial.write( GPS_SEPARATOR_END );
  
  //delay(50);
}

