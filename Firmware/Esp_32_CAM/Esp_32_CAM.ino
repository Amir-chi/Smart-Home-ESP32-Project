#include "Arduino.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#include "config.h"
#include "WiFiHandler.h"
#include "CameraHAL.h"
#include "FlashController.h"
#include "ServerComm.h"

WiFiHandler myWiFi;
CameraHAL camera;
FlashController flash;
ServerComm server(&flash, &camera);

void setup() {
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 
    
    Serial.begin(115200);
    delay(2000);
    
    Serial.println("\n--- SYSTEM START ---");
    Serial.printf("Free Heap: %d bytes\n", ESP.getFreeHeap());

    flash.begin();
    
    if(!camera.begin()){
        Serial.println("Camera Init Failed!");
        while(1) {
            delay(1000);
        }
    }
    
    myWiFi.begin();
    
    if(myWiFi.isConnected()){
        server.begin();
        Serial.println("Server started successfully");
    } else {
        Serial.println("WiFi not connected, server not started");
    }
    
    Serial.printf("Free Heap after init: %d bytes\n", ESP.getFreeHeap());
}

void loop() {

    if (!myWiFi.isConnected()) {
        Serial.println("WiFi disconnected! Attempting reconnect...");
        myWiFi.begin();
        delay(5000);
        return;
    }
    
    server.loop();
    

    static unsigned long lastMemCheck = 0;
    if (millis() - lastMemCheck > 30000) {
        Serial.printf("Free Heap: %d bytes\n", ESP.getFreeHeap());
        lastMemCheck = millis();
    }
    
    yield();
    delay(10);
}
