#include <Arduino.h>

// table 1 circuit design
// C_in: 4.7µF, 50V, 1206
// C_out: 4.7µF, 25V, 1210
// R_fb = 1.78k
// V_out = 24 V
// V_in: 2.8-21 V

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(7, HIGH);
  // wait for a second
  delay(1000);
  // turn the LED off by making the voltage LOW
  digitalWrite(7, LOW);
   // wait for a second
  delay(1000);
}