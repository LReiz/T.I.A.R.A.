const int relay = 9;
char previousState;
int currentWait = 0;
int maxWait = 5;
bool enableChangeState = true;

void setup() {
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);
  previousState = '1';
}

void loop() {
  if(Serial.available() > 0) {
    char eyesFound = Serial.read();
    
    if(previousState == eyesFound) {
      currentWait += 1; 
    } else {
      currentWait = 0;
    }
    
    if(currentWait >= maxWait) {
      currentWait = 0;
      enableChangeState = true;
    }
    
    previousState = eyesFound;
  
  
    if(enableChangeState) {
      if(eyesFound == '1') {
        digitalWrite(relay, HIGH);   
      } else {
        digitalWrite(relay, LOW);
      }
      enableChangeState = false;
    }
  }
}
