#include <Arduino.h>
#line 1 "C:\\Users\\enzo\\OneDrive\\Documentos\\Arduino\\Mecanum\\Mecanum.ino"
#line 1 "C:\\Users\\enzo\\OneDrive\\Documentos\\Arduino\\Mecanum\\Mecanum.ino"
void setup();
#line 6 "C:\\Users\\enzo\\OneDrive\\Documentos\\Arduino\\Mecanum\\Mecanum.ino"
void loop();
#line 1 "C:\\Users\\enzo\\OneDrive\\Documentos\\Arduino\\Mecanum\\Mecanum.ino"
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() { 
  // put your main code here, to run repeatedly:
  Serial.println("Mecanum");
  delay(20);
}

