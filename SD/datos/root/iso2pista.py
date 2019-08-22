
import os
import signal
import requests
import time
import sys
  
data = bytearray(4)

# Datos de acceso a Adafruit
API_DATA_TEMP = "https://io.adafruit.com/api/v2/pista86/feeds/temp/data"
API_DATA_HUM = "https://io.adafruit.com/api/v2/pista86/feeds/hum/data"
API_KEY = "a2e11cf933ba4a548d10684762dd4393"

header = {'X-AIO-Key': API_KEY}

def receiveSignal(signalNumber, frame):
    os.close(fd)
    print("Device cerrado") 
    sys.exit()

def sendHum(humVal):
    datos = {'value':'{0:.2f}'.format(humVal)} 
    r = requests.post(url = API_DATA_HUM, data=datos, headers=header)
    # debug
    print(r.text) 
    print("Humedad enviada a servidor:%0.2f"%humVal) 

def sendTemp(tempVal):
    datos = {'value':'{0:.2f}'.format(tempVal)} 
    r = requests.post(url = API_DATA_TEMP, data=datos, headers=header)
    # debug 
    print(r.text)
    print("Temperatura enviada a servidor:%0.2f"%tempVal) 

# Registrar handler de señal
signal.signal(signal.SIGINT, receiveSignal)

# Apertura de device
fd = os.open("/dev/i2c-pistahtu21d",os.O_RDWR)


if (fd != 0):
    print("Device abierto") 
    medirTyH = 1
    resol = 14
    os.write(fd, resol.to_bytes(1, byteorder='big', signed=False))


while (medirTyH):

    os.readv(fd, [data])

    if len(data) == 4 :
        humedad = ((data[1] << 8) + data[0]) & 0xFFFC
        temperatura = ((data[3] << 8) + data[2]) & 0xFFFC

        humedadFloat = ((humedad * 125.0) / 65536) - 6
        temperaturaFloat = ((temperatura * 175.72) / 65536) - 46.85

        sendHum(humedadFloat)
        time.sleep(10)
        sendTemp(temperaturaFloat)

    time.sleep(10)

