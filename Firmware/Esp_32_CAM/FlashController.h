#ifndef FLASH_CONTROLLER_H
#define FLASH_CONTROLLER_H
#include <Arduino.h>
#include "config.h"
class FlashController {
public:
    void begin() { pinMode(FLASH_PIN, OUTPUT); digitalWrite(FLASH_PIN, LOW); }
    void turnOn() { digitalWrite(FLASH_PIN, HIGH); Serial.println("[ESP_32_CAM] Flash ON"); }
    void turnOff() { digitalWrite(FLASH_PIN, LOW); Serial.println("[ESP_32_CAM] Flash OFF"); }
};
#endif