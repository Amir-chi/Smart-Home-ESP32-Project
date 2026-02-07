<h1 align="center">🏠 ESP32-CAM Based Smart Home System</h1>
<h3 align="center">Final IoT Project</h3>

<p align="center">
A modern <strong>Internet of Things (IoT)</strong> smart home system based on
<strong>ESP32-CAM</strong> that allows users to control devices using
<strong>natural language commands</strong> powered by Artificial Intelligence.
</p>

<p align="center">
🎓 Final Project – Internet of Things (IoT) Course
</p>

---

## 📌 Project Overview

Traditional smart home systems rely on fixed buttons or predefined commands.
This project introduces an **AI-powered Smart Home System** capable of understanding
**natural language commands in Persian and English**.

Users can interact with the system through a web-based dashboard and control
virtual devices as well as the ESP32-CAM camera features.

---

## 🔹 Interaction Methods

- 🌐 Web Dashboard  
- 📝 Text Commands  
- 🎙️ Voice Commands  
- ✋ Image / Gesture Commands   
- 🤖 Telegram Bot   

---

## ✨ Features


- 🌐 **Web-Based User Interface**
  - Command input box
  - Device status visualization

- 🧠 **AI Command Processing**
  - LLM-based natural language understanding
  - Persian & English support

- 💡 **Virtual Lamp Control**
  -  independent virtual lamps
  - Visual ON/OFF state

- 🔦 **Camera Flash Control**
  - ON / OFF via AI commands

- 📸 **Photo Capture**
  - ESP32-CAM image capture
  - Display last captured image

---

## 🔹 Responsibilities

### ESP32-CAM
- Camera image capture
- Flash control
- Wi-Fi communication
- Works in:
  - Station Mode (Internet access)
  - Access Point Mode (Local web access)

### Python Server
- REST API endpoints
- AI command processing
- Device state management
- Database operations
- Communication with ESP32-CAM

---

## 🧠 AI Command Processing Flow

1. User sends a command
2. Command is sent to the AI API
3. AI extracts intent and device
4. Structured command is generated

---

## 🧱 System Architecture

```
User Interface
      ↓
Python Server
      ↓
AI Services (LLM / Vision)
      ↓
ESP32-CAM
```

---

## 🛠️ Technology Stack

- **Hardware:**
ESP32-CAM

- **Backend:** 
Python (FastAPI / Django)

- **Frontend:** 
HTML, CSS, JavaScript

- **AI:**
 LLM, Speech-to-Text, Vision AI
 
- **Database:**
 Command & Image history

---

## 🌍 Deployment

✅ Real production server  
✅ Not local-only  
✅ Web accessible

---

## ✅ Conclusion

A complete, production-level **IoT Smart Home System** combining:

- Embedded Systems  
- Artificial Intelligence  
- Web Technologies  
- Cloud Deployment

---

⭐ Thank you for reviewing this project.
