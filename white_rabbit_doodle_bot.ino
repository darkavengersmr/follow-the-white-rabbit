#define RightNapr  8
#define RightSpeed 10  

#define RightLight A0
#define LeftLight A1  

#define LeftNapr  7    // Left  motor direction control pin
#define LeftSpeed  9    // Left  motor pulse width modulation pin

#define ServoPen 12    // Servo to raise / lower pen
#define Battery  7    // Battery voltage monitor pin (analog input)

#include <Servo.h>
Servo myservo;

float e = 0;
float u = 0;
float P = 0.02;
float D = 0.06;
int speedL = 0;
int speedR = 0;
int speedM = 55;

void setup() { 
  pinMode(RightNapr, OUTPUT);
  pinMode(RightSpeed, OUTPUT);
  pinMode(LeftNapr, OUTPUT);
  pinMode(LeftSpeed, OUTPUT);
 
}

void loop() { 
  int sensorL = analogRead(RightLight);
  int sensorR = analogRead(LeftLight);

  e = sensorL - (sensorR+150);
  u = e*P;
  speedR = speedM - u;
  speedL = speedM + u;

  if(speedR > 0){ digitalWrite(RightNapr, LOW); }
  else { digitalWrite(RightNapr, HIGH); }

  if(speedR > 255) { speedR = 255; }
  if(speedR < 0) { speedR = -1 * speedR; }
  
  analogWrite(RightSpeed, speedR);

  if(speedL > 0){ digitalWrite(LeftNapr, LOW); }
  else { digitalWrite(LeftNapr, HIGH); }

  if(speedL > 255) { speedL = 255; }
  if(speedL < 0) { speedL = -1 * speedL; }
  
  analogWrite(LeftSpeed, speedL);
  
}
