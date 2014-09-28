//Lectura de temperatura con sensor LM35

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
  temp = temp * 330 / 4096; //Conversion de ADC a temperatura
  Serial.println(temp);
  delay(500);
}
