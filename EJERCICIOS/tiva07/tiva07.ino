//Controlador ON-OFF
const byte PWM_PIN = 19; //Ventilador
const byte TEMP_SENSOR = A7; //LM35

const byte MAX_TEMP = 30;

void setup()
{
  pinMode(PWM_PIN, OUTPUT);
  digitalWrite(PWM_PIN, 0);
  
  pinMode(TEMP_SENSOR, INPUT);
  
}

uint32_t leeTemp(){
  uint32_t temp;
  temp = analogRead(TEMP_SENSOR);
  temp = temp * 330 / 4096;
  return temp;
}

void loop()
{
  uint32_t temp;
  temp = leeTemp();
  if(temp > MAX_TEMP){
    digitalWrite(PWM_PIN, 1);
  }else{
    digitalWrite(PWM_PIN, 0);
  }
  delay(1);  
}

