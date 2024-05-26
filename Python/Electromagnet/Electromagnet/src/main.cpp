#include <Arduino.h>

// table 1 circuit design
// C_in: 4.7µF, 50V, 1206
// C_out: 4.7µF, 25V, 1210
// R_fb = 1.78k
// V_out = 24 V
// V_in: 2.8-21 V

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    digitalWrite(7, HIGH);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
}