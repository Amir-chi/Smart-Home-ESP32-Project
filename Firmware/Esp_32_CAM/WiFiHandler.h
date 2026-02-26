#ifndef WIFI_HANDLER_H
#define WIFI_HANDLER_H

#include <WiFi.h>
#include "config.h"

class WiFiHandler {
public:
    void begin() {
        Serial.print("[WiFi] Connecting to: ");
        Serial.println(WIFI_SSID);
        
        WiFi.disconnect(true);
        delay(100);
        
        WiFi.mode(WIFI_STA);
        WiFi.setAutoReconnect(true);
        WiFi.begin(WIFI_SSID, WIFI_PASS);
        
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 30) {
            delay(500);
            Serial.print(".");
            attempts++;
        }
        
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("\n[WiFi] Connected!");
            Serial.print("IP: ");
            Serial.println(WiFi.localIP());
            Serial.print("Signal: ");
            Serial.println(WiFi.RSSI());
        } else {
            Serial.println("\n[WiFi] Connection Failed.");
        }
    }
    
    bool isConnected() {
        return WiFi.status() == WL_CONNECTED;
    }
};

#endif
