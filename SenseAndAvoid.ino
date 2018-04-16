#include <DualVNH5019MotorShield.h>

//library location /usr/share/arduino/libraries 

DualVNH5019MotorShield md;

// defines pins numbers
const int trigPinL = 43;
const int echoPinL = 45;
const int trigPinM = 47;
const int echoPinM = 49;
const int trigPinR = 51;
const int echoPinR = 53;
const int encodL = 16;
const int encodR = 17;

// defines variables
long durationL, durationM, durationR;
int distanceL, distanceM, distanceR;
int minDist = 30;                      //CM ???????
 
void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    while(1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    while(1);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();

  pinMode(trigPinL, OUTPUT); // Sets Left Sonar trigPin as Output
  pinMode(echoPinL, INPUT);  // Sets Left Sonar echoPin as Input
  pinMode(trigPinM, OUTPUT); // Sets Middle Sonar trigPin as Output
  pinMode(echoPinM, INPUT);  // Sets Middle Sonar echoPin as Input
  pinMode(trigPinR, OUTPUT); // Sets Right Sonar trigPin as Output
  pinMode(echoPinR, INPUT);  // Sets Right Sonar echoPin as Input
  pinMode(encodL, INPUT);    // Sets Left Encoder pin
  pinMode(encodR, INPUT);    // Sets Right Encoder pin
}

//turns the robot counterclockwise 45 degrees
/*
 * Sets speed to 0 to stop robot
 * First delay is used as a buffer so the robot loses momentum before turning
 * Sets the left wheel to reverse and the right wheel to go forward at a rate of 60
 * Second delay is to wait for the robot to turn for a set amount of time
 * Then it stops both wheels
 * Last delay is used as a buffer so the robot loses momentum before going forward
 */
void turnLeft() {
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(250);
  md.setM1Speed(100);
  md.setM2Speed(100);
  delay(500);
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(250);
}

//turns the robot clockwise 45 degrees
/*
 * Sets speed to 0 to stop robot
 * First delay is used as a buffer so the robot loses momentum before turning
 * Sets the left wheel to go forward and the right wheel to reverse at a rate of 60
 * Second delay is to wait for the robot to turn for a set amount of time
 * Then it stops both wheels
 * Last delay is used as a buffer so the robot loses momentum before going forward
 */
void turnRight() {
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(250);
  md.setM1Speed(-120);
  md.setM2Speed(-120);
  delay(500);
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(250);
}

//Sets speed of the robot to go forward at a user defined speed
void forward(int speed) {
  md.setM1Speed(-speed);
  md.setM2Speed(speed);
}

//Sets speed of the robot to reverse at a user defined speed
void reverse(int speed) {
  md.setM1Speed(speed);
  md.setM2Speed(-speed);
}

//Sets speed to 0 to stop robot from moving
//Delay used as buffer so the robot loses momentum
void brake() {
  md.setM1Speed(0);
  md.setM2Speed(0);
  delay(500);
}


void loop() {
  
  //Left Sonar
  digitalWrite(trigPinL, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinL, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinL, LOW);
  durationL = pulseIn(echoPinL, HIGH);
  distanceL = durationL*0.034/2;

  //Middle Sonar
  digitalWrite(trigPinM, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinM, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinM, LOW);
  durationM = pulseIn(echoPinM, HIGH);
  distanceM = durationM*0.034/2;
  
  //Right Sonar
  digitalWrite(trigPinR, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinR, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinR, LOW);
  durationR = pulseIn(echoPinR, HIGH);
  distanceR = durationR*0.034/2;
  

  if (distanceM <= minDist+5 || distanceR <= minDist) {
    reverse(25);
    delay(50);
    brake();
    turnLeft();
  } else if (distanceL <= minDist) {
    reverse(25);
    delay(50);
    brake();
    turnRight();
  } else {
    forward(100);
  }

  Serial.println("Left Ticks: "+digitalRead(encodL));
  Serial.println("Right Ticks: "+digitalRead(encodR));
  
  delay(100);
}
