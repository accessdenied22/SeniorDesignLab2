int outPin = 2;   // LED or buzzer connected to digital pin 2
int val = 0;      // variable to store the read value from the analog pin

int analogPin = A3; // Analog pin connected to the receiver and ADC

void setup() {
  Serial.begin(9600);
  pinMode(outPin, OUTPUT);  // sets the digital pin as output
}

void loop() {
  val = analogRead(analogPin);   // read the input analog pin from 0-1023
  Serial.print(val);
  Serial.print(",");  // Send analog values through USB as a comma separated list

  if(val < 150) {
    digitalWrite(outPin, HIGH);  // turns the buzzer on
  } else {
    digitalWrite(outPin, LOW);  // turns the buzzer off
  }
}
