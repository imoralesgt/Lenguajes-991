byte i;

void setup()
{
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  
  pinMode(PUSH1, INPUT_PULLUP);
  pinMode(PUSH2, INPUT_PULLUP);
  
  i = 0;
}

byte leds[3] = {RED_LED, GREEN_LED, BLUE_LED};



void loop()
{
  
  while(digitalRead(PUSH1)==1 && digitalRead(PUSH2)==1){
    ;
  }
    
  
  if(digitalRead(PUSH1) == 0){
    i = (i+1)%3; 
  }else if(digitalRead(PUSH2) == 0){
    i = (i-1)%3;
  }

  int j;
  for(j = 0; j < 3; j++){
    digitalWrite(leds[j], 0);
  }
  
  digitalWrite(leds[i], 1);
  
  delay(200);
  
}
