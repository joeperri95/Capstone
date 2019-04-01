int pump1 = 9; //OJ
int pump2 = 10; //GA
int levelsensor = A0;
int cupsensor = 8;
int dir = 11;
int elevator = 12;

void setup() {
  Serial.begin(9600);
  pinMode(pump1,OUTPUT);
  pinMode(pump2,OUTPUT);

  pinMode(dir,OUTPUT);
  pinMode(elevator,OUTPUT);
  
  pinMode(levelsensor,INPUT);
  pinMode(cupsensor,INPUT);
  
}

void loop() {
  test();
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

void elevatorUp(){
  digitalWrite(dir,HIGH);
}
void elevatorDown(){
  digitalWrite(dir,LOW);
}

void test(){
  if (analogRead(levelsensor) > 100){
    digitalWrite(pump1,HIGH);
  }
  else{
   digitalWrite(pump1,LOW);
  }
  delay(100);
  Serial.println(analogRead(levelsensor));
 }
