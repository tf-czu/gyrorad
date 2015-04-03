# gyrorad
Arduino-based Data Collector (multiple gyro+acc, GPS)


# GPS GY-GPS6MV2
- GPS data sheet
https://www.openimpulse.com/blog/wp-content/uploads/wpsc/downloadables/GY-NEO6MV2-GPS-Module-Datasheet.pdf

# ITG/MPU gyro  GY-521
- hit how to connect multiple I2C devices is here:
http://playground.arduino.cc/Main/MPU-6050#multiple

- store info (random)
https://www.dipmicro.com/store/GY521-MOD

- data sheet
http://www.invensense.com/mems/gyro/documents/PS-MPU-6000A-00v3.4.pdf

# Arduino Uno
I2C pins A4 (SDA), A5 (SCL)
http://arduino.cc/en/reference/wire

# Wiring ver0
GyroBoard: SCL - GREEN - A5, 5V - BLUE

GPS: GND - BLACK, 3.3V - RED, TX-BLUE-pin2, RX-GREEN-pin3


# External Arudino Libraries

BMSerial is used from project FireAnt from Orion Robotics:
http://downloads.orionrobotics.com/downloads/code/arduino.zip

