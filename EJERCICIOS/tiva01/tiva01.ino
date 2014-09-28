//Blinking LED

const byte myLED = 40;

void setup()
{
  pinMode(myLED, OUTPUT);
  digitalWrite(myLED, 0);
}

void loop()
{
  digitalWrite(myLED, 1);
  delay(500);
  digitalWrite(myLED, 0);
  delay(500);
}