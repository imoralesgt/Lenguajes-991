//Lectura de temperatura con sensor LM35
//Utilizando una cifra decimal

const byte TEMP_PIN = A7;

void setup()
{
  pinMode(TEMP_PIN, INPUT); //No usa PULL-UP porque es entrada analogica
  Serial.begin(115200); //Inicializar UART (puerto serial) 
}

uint32_t temp; //Unsigned Integer de 32 bits

void loop()
{
  temp = analogRead(TEMP_PIN);
  temp = temp * 3300 / 4096; //Conversion de ADC a temperatura
  Serial.print(temp/10);
  Serial.print(".");
  Serial.println(temp%10);
  delay(500);
}
