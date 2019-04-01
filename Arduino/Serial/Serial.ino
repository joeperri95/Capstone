int r = 1;
void setup() {
  Serial.begin(9600);
}

void loop(){
  if(Serial.available()){         //From RPi to Arduino
    r = Serial.read() - '0';  //conveting the value of chars to integer
    if (r == 1){
      Serial.write(r+1);
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
      Serial.write(-1);
    }
  }
}
