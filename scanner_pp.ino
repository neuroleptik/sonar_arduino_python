#include <Servo.h>
#include <NewPing.h>

Servo radar; //moteur de base
NewPing sonar(2,4,200); // radar tournant

const int PIN_RADAR = 7;
const int PIN_BIP = 6;
const int DISTANCE_MIN = 50;
int distance = 0;


void setup() {
  radar.attach(PIN_RADAR);
  pinMode(PIN_BIP,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 180; i++){
    distance = getDistance();
    Serial.print(i);
    Serial.print(" ");
    Serial.println(distance);
    if (distance < DISTANCE_MIN && distance != 0){
      digitalWrite(PIN_BIP,HIGH);
      delay(30);
       digitalWrite(PIN_BIP,LOW);
    }
    radar.write(i);
  }
  for (int i = 180; i > 0; i--){
    distance = getDistance();
    Serial.print(i);
    Serial.print(" ");
    Serial.println(distance);
    if (distance < DISTANCE_MIN && distance != 0){
      digitalWrite(PIN_BIP,HIGH);
      delay(30);
      digitalWrite(PIN_BIP,LOW); 
    }
    radar.write(i);
  }
}

int getDistance(){
  delay(70);

  unsigned int uS = sonar.ping();
  int cm = uS/US_ROUNDTRIP_CM;

  return cm;
}
