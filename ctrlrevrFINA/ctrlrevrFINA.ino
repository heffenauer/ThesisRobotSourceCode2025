#include <AccelStepper.h>

#define DIR_PIN_LEFT   2
#define STEP_PIN_LEFT  3
#define DIR_PIN_RIGHT  4
#define STEP_PIN_RIGHT 5

// Create two driver steppers: left and right
AccelStepper stepperLeft (AccelStepper::DRIVER, STEP_PIN_LEFT, DIR_PIN_LEFT);
AccelStepper stepperRight(AccelStepper::DRIVER, STEP_PIN_RIGHT, DIR_PIN_RIGHT);

void setup() {
  Serial.begin(115200);
  stepperLeft. setMaxSpeed(500);
  stepperLeft. setAcceleration(500);
  stepperRight.setMaxSpeed(500);
  stepperRight.setAcceleration(500);
}

void loop() {
  // Check for a full line (ends at '\n')
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "start") {
      // Handshake: ensure both motors are stopped
      stepperLeft.stop();
      stepperRight.stop();
    }
    else if (cmd == "f") {
      // Forward: both motors
      stepperLeft. moveTo(-1000000);  // reversed for LEFT
      stepperRight.moveTo( 1000000);
    }
    else if (cmd == "b") {
      // Backward: both motors opposite
      stepperLeft. moveTo( 1000000);
      stepperRight.moveTo(-1000000);
    }
    else if (cmd == "f1") {
      // Pivot right: left motor only
      stepperLeft. moveTo(-1000000);
      stepperRight.stop();
    }
    else if (cmd == "f2") {
      // Pivot left: right motor only
      stepperRight.moveTo( 1000000);
      stepperLeft. stop();
    }
    else if (cmd == "r") {
      // In-place spin: wheels opposite
      stepperLeft. moveTo( 1000000);
      stepperRight.moveTo(-1000000);
    }
    else if (cmd == "l") {
      // In-place spin opposite direction
      stepperLeft. moveTo(-1000000);
      stepperRight.moveTo( 1000000);
    }
    else if (cmd == "s") {
      // Stop both
      stepperLeft.stop();
      stepperRight.stop();
    }
    // else: ignore unknown commands
  }

  // Always call run() so the steppers actually move toward their targets
  stepperLeft.run();
  stepperRight.run();
}
