#!/usr/bin/python

# Importamos la libreira de PySerial
import serial
import json
import threading
import time
import datetime
import os
import glob
import signal
import sys
import requests

def EnvioArchivo():
  path = '/home/pi/Desktop/Muestreos'
  #192.168.0.141 ip lab #######192.168.1.68 ip casa 
  url = 'https://www.labmovilidad.unam.mx/tesismonitor/api/test/data'
  headers = {'Authorization' : '(some auth code)', 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
  conteo = 0
  while True:
    #if len(glob.glob("/home/pi/Desktop/Muestreos/*.json")) == 5:
    if conteo >= 10:
      listFiles = []
      listDir = os.walk(path)  
      for root, dirs, files in listDir:
        for fichero in files:
          #(nombreFichero, extension) = os.path.splitext(fichero)
          #if (extension == ".json"):
            #listFiles.append(nombreFichero+extension)
	  if fichero.endswith('.json'):
            listFiles.append(fichero)
      print (listFiles)

      for i in listFiles:
        #print (i)
        #dirSend = str(i)
	dirSend = open(path+'/'+i, 'rb').read()
        response = requests.post(url, data=dirSend, headers=headers)
        response.status_code

      print ("Listado final")
      print ("longitud de la lista = ", len(listFiles))
      time.sleep(1)
      if response.status_code == requests.codes.ok:
      	print ("Delete")
	BorrarArchivo()
    else:
      print ("aun no")
      conteo = conteo + 1
      time.sleep(1)


def BorrarArchivo():
  print ("borrando...")
  count = 0
  path = os.path.join("/home/pi/Desktop/Muestreos/")
  pattern = ".json"
  maxdepth = 1
  cpath=path.count(os.sep) 
  for r,d,f in os.walk(path):
      if r.count(os.sep) - cpath < maxdepth:
          for files in f:   
            if files.endswith(pattern):
                try:
                    print ("Removing %s" % (os.path.join(r,files)))
                    os.remove(os.path.join(r,files))
                except Exception,e:
                    print (e)
            else:
                print ("%s removed" % (os.path.join(r,files)))

def main ():
  x = 1
  envio = threading.Thread(target=EnvioArchivo)
  envio.setDaemon(True)
  envio.start()
  while True:
    try:
        time.sleep(.3)
        x += 1
    except KeyboardInterrupt:
        print ("Bye")
        sys.exit()

if __name__ == '__main__':
  main()


