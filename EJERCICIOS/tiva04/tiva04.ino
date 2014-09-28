
const byte ANALOG_IN = A11;
const byte LED_OUT = RED_LED;
const unsigned int UMBRAL = 500;

void setup()
{
  pinMode(ANALOG_IN, INPUT);
  pinMode(LED_OUT, OUTPUT);
  digitalWrite(LED_OUT, 0);
  Serial.begin(115200);
}

void loop()
{
  unsigned int analogico;
  analogico = analogRead(ANALOG_IN);
  if(analogico > UMBRAL){
    digitalWrite(LED_OUT, 1);
  }else{
    digitalWrite(LED_OUT, 0);
  }
  Serial.println(analogico, DEC);
  delay(100);
  
}

