"""MIT License

Copyright (c) 2024 Peavepuf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


###########################
### METEROLOGY ST. V2.4 ###
###########################

#LIBRARIES
from machine import Pin, I2C, ADC
import time,urequests,network
from bmp085 import BMP180
import dht
from rotary_irq_rp2 import RotaryIRQ
import ADS1115
#LIBRARIES
#-------------------------------------------- 
#INTERNET FUNC.
def wifi_baglan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Bağlantı bekleniyor...")
        wlan.connect(ssid, password)
        
        while not wlan.isconnected():
            pass
    
    print("Bağlantı başarılı!")
    print("IP Adresi:", wlan.ifconfig()[0])
#INTERNET FUNC.   
#-------------------------------------------- 
#INTERNET DETAIL DEFINITION
HTTP_HEADERS = {'Content-Type': 'application/json'} 
MeterologyAir = 'YOUR API KEY'
MeterologySoil = 'YOUR API KEY'  
ssid = YOUR SSID
password = YOUR PASSWORD
#INTERNET DETAIL DEFINITION
#--------------------------------------------
#STATUS FUNC.
def durum(kod):
    #DATA SEND-------------------------------------------------------
    durumkodu = {'status':kod}
    air=request = urequests.post( 'http://api.thingspeak.com/update?api_key='+ MeterologyAir, json = durumkodu,headers = HTTP_HEADERS )
    air.close
    #--                      
    soil=request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + MeterologySoil, json = durumkodu, headers = HTTP_HEADERS )
    soil.close
    #DATA SEND-------------------------------------------------------
    if kod=="Hata: E1" or kod=="Hata: E2" or kod=="Hata: E3" or kod=="Hata: E4":
        raise SystemExit("Program sonlandırıldı.")
    

#STATUS FUNC.
#--------------------------------------------
#PIN DEFINITION
TPRK=ADC(2)#SOIL MOISTURE SENSOR PIN GPIO28
dSensor = dht.DHT11(Pin(2))# DHT PİN GPIO2
ADS1115.init(0x48, 1, 4, False)#ADS DEFINITION
led=Pin('LED',Pin.OUT)

try:
    i2c1 = I2C(1, scl = Pin(7), sda = Pin(6),freq=40000)
    bmp = BMP180(i2c1)#BMP180 DEFINITION
    
except Exception as e:
    print("BMP ÇALIŞMIYOR")
    print("Error:", str(e))
    durum("ERROR: E1")
 
r = RotaryIRQ(pin_num_clk=12,#CLK PİN
              pin_num_dt=13,#DT PİN
              min_val=0, 
              max_val=359,
              incr=18,#STEP INCREASE
              half_step=False,
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
#PIN DEFINITION
#--------------------------------------------
#GLOBAL DEFINITION
global temp,hum,isik,rakim,basinc,tnem,yaprak2,ruzgaraci,yagmur
#GLOBAL DEFINITION
#-------------------------------------------- 
#MAP FUNC.
def MAP(x, giris_min, giris_max, cikis_min, cikis_max):
        return (x - giris_min) * (cikis_max - cikis_min) / (giris_max - giris_min) + cikis_min
#MAP FUNC.
#-------------------------------------------- 
#WIND DIRECTION MEASURE
def readRTR():
    global ruzgaraci
    ruzgaraci = r.value()
    val_old = r.value()
    print('Rüzgar Açısı:', ruzgaraci)
    if val_old != ruzgaraci:
        val_old = ruzgaraci
#WIND DIRECTION MEASURE
#--------------------------------------------   
#LEAF WETNESS AND RAIN CONDITION MEASUREMENT
def readRAIN():
    global yaprak2,yagmur
    try:
        a,rain,isikdeger,ruzgarhiz=ADS1115.readMulti(0,4)
        yaprak1=MAP(rain, 0, 26471, 100, 0)
        time.sleep(5)
        a,rain,isikdeger,ruzgarhiz=ADS1115.readMulti(0,4)
        yaprak2=MAP(rain, 0, 26471, 100, 0)
        if yaprak2<5:
            yaprak2=0
        print("\nYaprak Islaklığı:%",int(yaprak2))
        if yaprak2>yaprak1:
            if yaprak2-yaprak1>0.5 or yaprak2>40:
                print("***Yağmur Yağıyor+++++++")
                yagmur=1
            else:
                print("***Yağmur Yağmıyor------")
                yagmur=0
        else:
            print("***Yağmur Yağmıyor------")
            yagmur=0
        
    except OSError as e:
        durum("ERROR: E2")
#LEAF WETNESS AND RAIN CONDITION MEASUREMENT 
#-------------------------------------------- 
#SOIL MOISTURE
def readTPRK():
    global tnem
    tnem1=TPRK.read_u16()
    tnem=MAP(tnem1, 10000, 54800, 100, 0)
    if tnem<5:
        tnem=0
    elif tnem>100:
        tnem=100
    print("Toprak Nemi:",tnem)
#SOIL MOISTURE
#--------------------------------------------     
#BMP180 MEASUREMENT    
def readBMP():
     global basinc,rakim
     basinc1 = bmp.pressure
     rakim = int(bmp.altitude)
     basinc=basinc1/100
     print("Rakım:",int(rakim),"mt")
     print("Basınç:",basinc)
#BMP180 MEASUREMENT 
#--------------------------------------------  
#TEMPERATURE AND HUMIDTY MEASURE
def readDHT():
    global temp,hum
    try:
        dSensor.measure()
        temp = dSensor.temperature()
        hum = dSensor.humidity()
        print('Sıcaklık:{} C'.format(temp))
        print('Nem:%{} '.format(hum))
    except OSError as e:
        print('DHT11 Çalışmıyor')
        durum("ERROR: E3")
#TEMPERATURE AND HUMIDTY MEASURE
#--------------------------------------------    
#LIGHT LEVEL MEASURE 
def readLDR():
    global isik
    a,b,isikdeger,ruzgarhiz=ADS1115.readMulti(0,4)
    isik=MAP(isikdeger, 700, 26741, 0, 100)
    isik=int(isik)
    if isik<1:
        isik=0
    elif isik>100:
        isik=100
    print("Işık Seviyesi:%",isik)
#LIGHT LEVEL MEASURE
#--------------------------------------------
#WIND SPEED MEASURE
def ruzgarhizi(): 
    global ruzgarhiz
    a,b,isikdeger,ruzgarhiz1=ADS1115.readMulti(0,4)
    time.sleep(.2)
    a,b,isikdeger,ruzgarhiz2=ADS1115.readMulti(0,4)
    time.sleep(.2)
    a,b,isikdeger,ruzgarhiz3=ADS1115.readMulti(0,4)
    ruzgarhiz=(ruzgarhiz1+ruzgarhiz2+ruzgarhiz3)/3
    ruzgarhiz=abs(ruzgarhiz-65)
    if ruzgarhiz<=1:
        ruzgarhiz=0
    print("Rüzgar hızı:{}".format(ruzgarhiz))
#WIND SPEED MEASURE
#--------------------------------------------   
wifi_baglan(ssid, sifre)
durum("SYSTEM HAS BEEN STARTED")
while True:
    try:
         global temp,hum,isik,rakim,basinc,tnem,yaprak2,ruzgaraci,yagmur,ruzgarhiz
         readRAIN()
         readBMP()
         readDHT()
         readLDR()
         ruzgarhizi()
         readRTR()
         readTPRK()
         
         #DATA SEND-------------------------------------------------------
         
         airveriler = {'field1':temp, 'field2':hum, 'field3':yagmur,'field4':isik,'field5':ruzgaraci, 'field6':ruzgarhiz, 'field7':basinc, 'field8':rakim}
         air=request = urequests.post( 'http://api.thingspeak.com/update?api_key='+ MeterologyAir, json = airveriler,headers = HTTP_HEADERS )
         air.close()
         #--                 
         soilveriler = {'field1':tnem, 'field2':yaprak2}
         soil=request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + MeterologySoil, json = soilveriler, headers = HTTP_HEADERS )
         soil.close()
         #DATA SEND-------------------------------------------------------
         
         print("------------------DATA SENT----------------")
         led.value(1)
         time.sleep(2)
         led.value(0)
         time.sleep(1)
         led.value(1)
         time.sleep(2)
         led.value(0)
         time.sleep(48)
    except Exception as e:
         print("LOOP NOT RUN")
         durum("ERROR: E4")
