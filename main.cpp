#include <Arduino.h>

// LED Control Pins (adjust as needed)
#define LED1 12  // GPIO12
#define LED2 13  // GPIO13
#define LED3 14  // GPIO14
#define LED4 15  // GPIO15

void setup() {
  Serial.begin(115200);
  
  // Initialize LED pins
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  
  // Initial state: LEDs 1 & 2 ON, 3 & 4 OFF
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, LOW);
  digitalWrite(LED4, LOW);
  
  Serial.println("System Ready - Monitoring for detection signals...");
}

void loop() {
  if (Serial.available()) {
    char signal = Serial.read();
    
    if (signal == '1') {
      // Object detected - TURN ON 3 & 4, TURN OFF 1 & 2
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, HIGH);
      digitalWrite(LED4, HIGH);
      Serial.println("DETECTED: LEDs 3-4 ON, LEDs 1-2 OFF");
    } 
    else if (signal == '0') {
      // No object - TURN ON 1 & 2, TURN OFF 3 & 4
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, LOW);
      Serial.println("CLEAR: LEDs 1-2 ON, LEDs 3-4 OFF");
    }
  }
}

