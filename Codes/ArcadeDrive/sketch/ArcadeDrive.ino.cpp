#include <Arduino.h>
#line 1 "C:\\Users\\enzo\\AppData\\Local\\Temp\\.arduinoIDE-unsaved2024219-20092-1yblp4.ce6ne\\ArcadeDrive\\ArcadeDrive.ino"
#include "stemOSboard.h"


// Use #define TELEOPERADO for teleop and AUTONOMO for autonomous

#define TELEOPERADO

stemWiFi wifi;

#line 10 "C:\\Users\\enzo\\AppData\\Local\\Temp\\.arduinoIDE-unsaved2024219-20092-1yblp4.ce6ne\\ArcadeDrive\\ArcadeDrive.ino"
void setup();
#line 21 "C:\\Users\\enzo\\AppData\\Local\\Temp\\.arduinoIDE-unsaved2024219-20092-1yblp4.ce6ne\\ArcadeDrive\\ArcadeDrive.ino"
void loop();
#line 48 "C:\\Users\\enzo\\AppData\\Local\\Temp\\.arduinoIDE-unsaved2024219-20092-1yblp4.ce6ne\\ArcadeDrive\\ArcadeDrive.ino"
void userCodeTeleopLoop(void * arg);
#line 10 "C:\\Users\\enzo\\AppData\\Local\\Temp\\.arduinoIDE-unsaved2024219-20092-1yblp4.ce6ne\\ArcadeDrive\\ArcadeDrive.ino"
void setup() {
  Serial.begin(115200);
  wifi.configureWiFiAP();

  delay(100);

  //esp_ipc_call(PRO_CPU_NUM, userCodeTeleopInit, NULL);
  estado = wifi.waitForStart();
  Serial.println(estado);
}

void loop() {
  String stat = wifi.getEnable();

  #ifdef TELEOPERADO
    wifi.getGamepadValues();
  #endif

  if(estado) {
    esp_ipc_call(PRO_CPU_NUM, userCodeTeleopLoop, NULL);
  }
  if(stat == "Habilitado") {
    estado = true;
  } else if(stat == "Desabilitado") {
    estado = false;
  }
}

// =============================================
//          CÓDIGO-DO-USUÁRIO ABAIXO
// =============================================

Gamepad gamepad;

Motor motorEsquerdaFrente(Motor::PORTA_1, Motor::REVERSE);
Motor motorEsquerdaTras(Motor::PORTA_2, Motor::REVERSE);

// Código do usuário que executará em loop
void userCodeTeleopLoop(void * arg) {
  #ifdef TELEOPERADO
    float y = gamepad.getLeftAxisY();
    float turn = gamepad.getRightAxisX();

    double frontLeftPower = (y + turn);
    double backLeftPower = (y - turn);

    double maximum = max(abs(frontLeftPower), abs(backLeftPower));

    frontLeftPower /= maximum;
    backLeftPower /= maximum;

    motorEsquerdaFrente.setPower(frontLeftPower);
    motorEsquerdaTras.setPower(backLeftPower);
  #else 
    Serial.println("Habilitado Arcade Drive");
  #endif
    //esp_ipc_call(APP_CPU_NUM, updateIMU, NULL);
}

// Caso você queira utilizar um IMU utilize essa função junto do seu código
/*
void updateIMU(void * arg) {
  imu.update();
}
*/


