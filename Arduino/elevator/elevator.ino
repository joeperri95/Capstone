int dir = 9;
int elevator = 10;

void setup() {
  Serial.begin(9600);
  pinMode(dir,OUTPUT);
  pinMode(elevator,OUTPUT);

}

void loop() {


}


void up(){
  int i;
  digitalWrite(dir,HIGH);
  
  for (i = 0; i<255; i++){
    analogWrite(elevator,i);
    delay(1);
  }
  
  delay(100);
  
  for (i = 255; i == 0; i--){
    analogWrite(elevator,i);
    delay(1)
  }
}
