#ifndef SERVER_COMM_H
#define SERVER_COMM_H

#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "FlashController.h"
#include "CameraHAL.h"

class ServerComm {
private:
    WebSocketsClient webSocket; 
    FlashController* flash;
    CameraHAL* camera;
    static ServerComm* instance;
    unsigned long lastPingTime = 0;
    bool isProcessing = false; // پرچم برای جلوگیری از پردازش همزمان

public:
    ServerComm(FlashController* f, CameraHAL* c) : flash(f), camera(c) {
        instance = this; 
    }

    void begin() {
    Serial.println("[Server] Configuring WebSocket...");
    webSocket.beginSSL(WS_HOST, WS_PORT, WS_PATH);
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(5000);
    
    // ✅ کاهش زمان heartbeat به 5 ثانیه
    webSocket.enableHeartbeat(5000, 3000, 2);
}

void loop() {
    webSocket.loop();
    
    // ✅ ارسال ping هر 5 ثانیه (به جای 30 ثانیه)
    if (millis() - lastPingTime > 5000) {
        webSocket.sendPing();
        lastPingTime = millis();
        Serial.println("[WS] Ping sent"); // اضافه کردن log
    }
}


    static void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
        if (instance) instance->handleEvent(type, payload, length);
    }

    void handleEvent(WStype_t type, uint8_t * payload, size_t length) {
        switch(type) {
            case WStype_DISCONNECTED:
                Serial.println("[WebSocket] Disconnected!");
                isProcessing = false;
                break;
            case WStype_CONNECTED:
                Serial.println("[WebSocket] Connected!");
                sendLogin();
                isProcessing = false;
                break;
            case WStype_TEXT:
                Serial.printf("[WebSocket] CMD: %s\n", payload);
                processCommand((char*)payload);
                break;
            case WStype_ERROR:
                Serial.println("[WebSocket] Error!");
                isProcessing = false;
                break;
            case WStype_PING:
                Serial.println("[WebSocket] Ping received");
                break;
            case WStype_PONG:
                Serial.println("[WebSocket] Pong received");
                break;
        }
    }

    void processCommand(char* jsonString) {
        if (isProcessing) {
            Serial.println("[Warning] Busy processing previous command");
            return;
        }
        
        isProcessing = true;

        String cleanJson = String(jsonString);

        if (cleanJson.startsWith("\"") && cleanJson.endsWith("\"")) {
            cleanJson = cleanJson.substring(1, cleanJson.length() - 1);
        }
        cleanJson.replace("\\\"", "\"");
        
        StaticJsonDocument<512> doc;
        DeserializationError error = deserializeJson(doc, cleanJson);

        if (error) {
            Serial.println("[Error] JSON Parse Failed");
            isProcessing = false;
            return;
        }
        bool settingsChanged = false;
        
        if (doc.containsKey("quality")) {
            int q = doc["quality"];
            Serial.printf("[Settings] Quality set to %d\n", q);
            camera->setQuality(q);
            settingsChanged = true;
        }

        if (doc.containsKey("brightness")) {
            int b = doc["brightness"];
            Serial.printf("[Settings] Brightness set to %d\n", b);
            camera->setBrightness(b);
            settingsChanged = true;
        }

        if (doc.containsKey("contrast")) {
            int c = doc["contrast"];
            Serial.printf("[Settings] Contrast set to %d\n", c);
            camera->setContrast(c);
            settingsChanged = true;
        }
        
        if (settingsChanged) {
            delay(200);
            yield();
        }

        if (doc.containsKey("action")) {
            String action = doc["action"].as<String>();
            
            if (action == "flash_on") {
                flash->turnOn();
                sendAck("flash_on");
            }
            else if (action == "flash_off") {
                flash->turnOff();
                sendAck("flash_off");
            }
            else if (action == "capture") {
                bool useFlash = false;
                if (doc.containsKey("flash")) {
                    String flashState = doc["flash"].as<String>();
                    useFlash = (flashState == "on");
                }
                sendPhoto(useFlash);
            }
        }
        
        isProcessing = false;
    }

    void sendLogin() {
        webSocket.sendTXT("{\"type\":\"login\", \"device\":\"ESP32-CAM\"}");
    }

    void sendAck(const char* action) {
        char buffer[100];
        snprintf(buffer, sizeof(buffer), "{\"type\":\"ack\", \"action\":\"%s\"}", action);
        webSocket.sendTXT(buffer);
    }

    void sendPhoto(bool withFlash = false) {
        Serial.println("[Camera] Capturing...");
        
        if (withFlash) {
            flash->turnOn();
            delay(100);
        }
        
        yield();
        
        camera_fb_t * fb = camera->takePicture();
        
        if (withFlash) {
            flash->turnOff();
        }
        
        if(!fb) {
             Serial.println("[Error] Capture failed");
             sendAck("capture_failed");
             return;
        }
        
        Serial.printf("[WebSocket] Sending Photo (%u bytes) in one chunk...\n", fb->len);
        
        webSocket.sendBIN(fb->buf, fb->len);
        
        camera->releasePicture(fb);
        sendAck("capture_success");
        
        Serial.println("[Camera] Photo sent successfully");
    }
};

ServerComm* ServerComm::instance = nullptr;

#endif
