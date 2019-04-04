int dir = 0;
int elevator = 6;

void setup() {
  Serial.begin(9600);
  pinMode(dir,OUTPUT);
  pinMode(elevator,OUTPUT);

}

void loop() {
  elevatorControl(1);
  while (1 == 1){
    
  }
}


void elevatorControl(int dirCtrl){
  int i;
  int j;
  digitalWrite(dir,dirCtrl);
  
  for (i = 1; i<255; i++){
    analogWrite(elevator,i);
    delay(10);
  }
  delay(75);
  
  for (j = 255; j > 0; j--){
    analogWrite(elevator,j);
    delay(10);
  }
  analogWrite(elevator,0);
}
