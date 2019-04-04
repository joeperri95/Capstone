int pump1 = 9; //Orange Juice
int pump2 = 10; //Ginger Ale
int levelsensor = A0;
int cupsensor = 8;
int dir = 11;
int elevator = 12;
int r = 0; //Recieved Order

void setup() {
  Serial.begin(9600);
  pinMode(pump1,OUTPUT);
  pinMode(pump2,OUTPUT);

  pinMode(dir,OUTPUT);
  pinMode(elevator,OUTPUT);
  
  pinMode(levelsensor,INPUT);
  pinMode(cupsensor,INPUT);
  
}

void loop(){
  if(Serial.available()){         //make sure we have serial connection
    r = Serial.read() - '0';     //convert incoming ASCII to integer
    
    if (r == 1){
      Serial.write(r+1);         // each if sends an echo and then a
      oj();
      Serial.write(5);
    }
    
    if(r == 2){
      Serial.write(r+2);
      Serial.write(5);
    }
    
    if(r == 3){
      Serial.write(r+3);
      Serial.write(5);
    }
    
    else{  
      Serial.write(-1);            // sends back a -1 if there are errors
    }
  }
}


void oj(){
  if (analogRead(levelsensor) > 100){
    digitalWrite(pump1,HIGH);
  }
  else{
   digitalWrite(pump1,LOW);
  }
  delay(100);
  Serial.println(analogRead(levelsensor));
}


void ga(){
  if (analogRead(levelsensor) > 100){
    digitalWrite(pump2,HIGH);
  }
  else{
   digitalWrite(pump2,LOW);
  }
  delay(100);
  Serial.println(analogRead(levelsensor));
}


void mimosa(){
  if (analogRead(levelsensor) > 100){
    digitalWrite(pump1,HIGH);
    digitalWrite(pump2,HIGH);
  }
  else{
   digitalWrite(pump1,LOW);
   digitalWrite(pump2,LOW);
  }
  delay(100);
  Serial.println(analogRead(levelsensor));
}
