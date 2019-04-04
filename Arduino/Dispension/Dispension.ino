int pump1 = 9; //Orange Juice
int pump2 = 10; //Ginger Ale
int cupsensor = 8;
int r = 0; //Recieved Order

void setup() {
  Serial.begin(9600);
  pinMode(pump1,OUTPUT);
  pinMode(pump2,OUTPUT);

  digitalWrite(pump1,LOW);
  digitalWrite(pump2,LOW);

  pinMode(cupsensor,INPUT);
  
}

void loop(){
  if(Serial.available()){        //make sure we have serial connection
    r = Serial.read() - '0';     //convert incoming ASCII to integer
    
    if (r == 1){
      Serial.write(r+1);         // each if sends an echo
      oj();                      // then dispenses drink
      Serial.write(5);           // then a success code
    }
    
    if(r == 2){
      Serial.write(r+2);
      ga();
      Serial.write(5);
    }
    
    if(r == 3){
      Serial.write(r+3);
      mimosa();
      Serial.write(5);
    }
    
    else{  
      Serial.write(-1);          // sends back a -1 if there are errors
    }
  }
}


void oj(){
  digitalWrite(pump1,HIGH);
  delay(32000);
  digitalWrite(pump1,LOW);
}


void ga(){
  digitalWrite(pump2,HIGH);
  delay(60000);
  digitalWrite(pump2,LOW);
}


void mimosa(){
  digitalWrite(pump1,HIGH);
  digitalWrite(pump2,HIGH);
  delay(24000);
  digitalWrite(pump1,LOW);
  digitalWrite(pump2,LOW);
}
