void setup() {
  
  Serial.begin(115200);
  analogReference(INTERNAL);
}

void loop() {

  //int adc = analogRead(A0); 
  //Serial.println(adc);
  float Irms=get_corriente(); //Corriente eficaz (A)
  //float P=Irms*120.0; // P=IV (Watts)
  //delay(30);
  //Serial.print("Irms: ");
  Serial.println(Irms,3);
  //Serial.print("A, Potencia: ");
  //Serial.print(P,3);  
  //Serial.println("W");
  //delay(100);     
}

float get_corriente()
{
  float voltajeSensor;
  float corriente=0;
  float Sumatoria=0;
  long tiempo=millis();
  int N=0;
  while(millis()-tiempo<500)//Duración 0.5 segundos(Aprox. 30 ciclos de 60Hz)
  { 
    
    voltajeSensor = analogRead(A0) * (1.1 / 1023.0);////voltaje del sensor
    //Serial.println(voltajeSensor);
    corriente=voltajeSensor*30.0; //corriente=VoltajeSensor*(30A/1V)
    
    Sumatoria=Sumatoria+sq(corriente);//Sumatoria de Cuadrados
    N=N+1;
    delay(1);
  }
  Sumatoria=Sumatoria*2;//Para compensar los cuadrados de los semiciclos negativos.
  corriente=sqrt((Sumatoria)/N); //ecuación del RMS
  return(corriente);
}
