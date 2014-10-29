//Sensor de presion atmosferica y temperatura (BMP180)
//Utilizado tambien para calcular altura (msnm)
//Descargar libreria de: https://github.com/astuder/BMP085-template-library-Energia

#include <Wire.h>          // Requerida por BMP085/BMP180 para I2C
#include <BMP085_t.h>
#include <math.h>

BMP085<0> PSensor;         // Instancia del sensor. Utilizar Puerto I2C #3

void setup()
{
  Serial.begin(9600);      // initialize serial, used to display readings in Serial Monitor
  Wire.begin();            // initialize I2C that connects to sensor
  PSensor.begin();         // initalize pressure sensor
}

float getAltitude(float press, float temp) {
  const float Po = 1013.25;
  return ((pow((Po / press), 1/5.257) - 1.0) * (temp + 273.15)) / 0.0065;
}

void loop()
{
  long h, t, p;
  PSensor.refresh();                    // Leer datos crudos del sensor
  PSensor.calculate();                  // Hacer calculo de presion y temperatura
  t = PSensor.temperature;              //Temperatura en Grados Celsius*10
  p = PSensor.pressure + 50;            //Presion en Pascales
  h = getAltitude((float)p/100, (float)t/10); //Hacer calculo de altitud
  Serial.print("Temperatura: ");         
  Serial.print(t/10);  // display temperature in Celsius
  Serial.print(".");
  Serial.print(t%10);  // display temperature in Celsius
  Serial.println("C");
  Serial.print("Presion:    ");
  Serial.print(p/100);   // display pressure in hPa
  Serial.println("hPa");
  Serial.print("Altitud:    ");
  Serial.print(h);
  Serial.println(" msnm");

  delay(5000);                          // Tomar una medicion no menos de 5 segundos despues de la actual
}

