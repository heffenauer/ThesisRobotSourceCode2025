void setup() {
  pinMode(2, OUTPUT);  // DIR pin
  pinMode(3, OUTPUT);  // STEP pin

  digitalWrite(2, LOW);  // Set direction LOW
  delay(500);

  for (int i = 0; i < 1000; i++) {
    digitalWrite(3, HIGH);
    delayMicroseconds(500);
    digitalWrite(3, LOW);
    delayMicroseconds(500);
  }

  delay(2000);

  digitalWrite(2, HIGH);  // Change direction
  delay(500);

  for (int i = 0; i < 1000; i++) {
    digitalWrite(3, HIGH);
    delayMicroseconds(500);
    digitalWrite(3, LOW);
    delayMicroseconds(500);
  }
}

void loop() {}
