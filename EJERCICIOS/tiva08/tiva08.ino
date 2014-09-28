//Controlador por histeresis

const byte PWM_PIN = GREEN_LED; //Ventilador
const byte TEMP_SENSOR = A7; //LM35

const byte TH = 32;
const byte TL = 26;

int currentState; //0 = OK, -1 = ABAJO, 1 = ARRIBA
byte out; //(Des)activa el ventilador

void setup()
{
  out = 0;
  pinMode(PWM_PIN, OUTPUT);
  digitalWrite(PWM_PIN, out);
  
  
  Serial.begin(115200);
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
  if(temp < TL){
    currentState = -1;
    out = 0; //Apagar el ventilador
  }else if(temp > TH){
    currentState = 1;
    out = 1; //Encender el ventilador
  }else{
    currentState = 0;
    out = out; //Mantener el valor anterior
  }
  
  digitalWrite(PWM_PIN, out);
  Serial.println(temp);
  delay(1);
  
}  
