//Distance sensor HC-SR04 + Frequency Output (THEREMIN)

#include <wiring_private.h> //Para usar PWMWrite, en vez de analogWrite

const byte ECHO_PIN = 9; //PA6
const byte TRIGGER_PIN = 10; //PA7
const byte AUDIO_PIN = 15; //PB7

long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 58;
}

long readEcho(){
  
  long microseconds;
  
  digitalWrite(TRIGGER_PIN, 1);
  delayMicroseconds(5);
  digitalWrite(TRIGGER_PIN, 0);
  microseconds = pulseIn(ECHO_PIN, 1);
  return microseconds;
  
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, 0);
  pinMode(ECHO_PIN, INPUT);
  pinMode(AUDIO_PIN, OUTPUT);
  digitalWrite(AUDIO_PIN, 0);
}

void loop()
{
  long duration, cm;

  duration = readEcho();

  cm = microsecondsToCentimeters(duration);
  PWMWrite(AUDIO_PIN, 255, 127, (cm+100)*4); //PIN, RESOLUTION, DUTY CYCLE, FREQUENCY

  Serial.print(cm);
  Serial.println("cm");
  
  delay(25);
}

