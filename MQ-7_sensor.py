#!/usr/bin/python
import time
import datetime
import mysql.connector

# Adafruiti raamatukogu
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Andmed adafruiti mikrokiibilt
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Mysql serveriga yhendamine
mydb = mysql.connector.connect(
  host="DB_HOST", 
  user="DB_USER",
  passwd="DB_PASSWORD",
  database="DB_NAME"
)
if mydb.is_connected():
  db_info = mydb.get_server_info()
  print (db_info)
else:
  print ("Ei saa serveriga yhendust!")

mycursor = mydb.cursor()

while True:

    #Muutujate kirjeldamine
    i=0
    k=0
    values=0

    #kuupaeva ja kellaja määramine
    kuupaev = str(datetime.datetime.now())
    aeg = datetime.datetime.utcnow()

   
    while k<120:
        values += mcp.read_adc(0)
        i+=1
        k+=1
        if i==5:
            values = values/5
            values = 5.85*2.718^(0.0182*values)-305
            i=0
            print(values)
            #muutujate lisamine andmebaasi
            mycursor.execute("INSERT INTO comootja (kuupaev, Ppm) VALUES (%s, %s)", (aeg.strftime('%Y-%m-%d %H:%M:%S'),values))
            mydb.commit()
            values=0
            time.sleep(10)
