import serial

PuertoSerie = serial.Serial('/dev/ttyUSB0',9600)

while True:
  sArduino = PuertoSerie.readline()
  print "Valor Arduino: " + sArduino.rstrip('\n')
