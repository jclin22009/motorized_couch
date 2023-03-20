#define leftMotor 5
#define rightMotor 3

#define speedMin 0
#define speedMax 100
#define leftMotorMin 55
#define leftMotorMax 175
#define rightMotorMin 55
#define rightMotorMax 175

int speed = 0;
int currentLeftSpeed = 0;
int currentRightSpeed = 0;
void setSpeed(int leftSpeed, int rightSpeed) {
  leftSpeed = constrain(leftSpeed, speedMin, speedMax);
  int leftPower = map(leftSpeed, speedMin, speedMax, leftMotorMin, leftMotorMax);
  rightSpeed = constrain(rightSpeed, speedMin, speedMax);
  int rightPower = map(rightSpeed, speedMin, speedMax, rightMotorMin, rightMotorMax);
  analogWrite(leftMotor, leftPower);
  analogWrite(rightMotor, rightPower);
}

void setup() {
  pinMode(leftMotor, OUTPUT);
  pinMode(rightMotor, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(1);
  // setSpeed(100, 100);
  // delay(250);
  // setSpeed(15, 15);
  // delay(250);
  // setSpeed(10, 10);
}

bool up = true;
int leftSpeed = 0;
int rightSpeed = 0;
void loop() {
  if (Serial.available() != 0) {
    // setSpeed(0, 0);
    leftSpeed = Serial.parseInt();
    rightSpeed = Serial.parseInt();
    Serial.print("Left speed: ");
    Serial.print(leftSpeed);
    Serial.print(", Right speed: ");
    Serial.println(rightSpeed);
  }

  // if (currentLeftSpeed < leftSpeed) {
  //   currentLeftSpeed++;
  // } else if (currentLeftSpeed > leftSpeed) {
  //   currentLeftSpeed--;
  // }

  // if (currentRightSpeed < rightSpeed) {
  //   currentRightSpeed++;
  // } else if (currentRightSpeed > rightSpeed) {
  //   currentRightSpeed--;
  // }

  // if (leftSpeed != currentLeftSpeed || rightSpeed != currentRightSpeed) {
  //   setSpeed(20, 20);
  // }

  currentLeftSpeed = leftSpeed;
  currentRightSpeed = rightSpeed;

  // delay(250);
  setSpeed(currentLeftSpeed, currentRightSpeed);
  delay(100);
}