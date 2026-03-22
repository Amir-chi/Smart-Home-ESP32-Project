# Smart Home Automation System with AI Integration

This project is a comprehensive Smart Home solution that bridges the gap between hardware (ESP32), web interfaces, and AI-driven controls. It was developed as a flagship project during our academic studies to demonstrate the power of IoT and Artificial Intelligence in modern living.

---

## 🚀 Overview
Unlike many local-only IoT projects, this system is deployed on a live production environment using **Liara Cloud**, making it accessible from anywhere. The core architecture is built on **Django**, with a dynamic **JavaScript** frontend and real-time hardware communication via **WebSockets**.

## ✨ Key Features
- **AI Command Line:** A natural language interface to control physical and virtual devices.
- **Voice Control:** Execute commands directly through the web UI using voice recognition.
- **Hand Gesture Recognition:** Control lighting through computer vision (OpenCV/MediaPipe logic):
  - 1 Finger: Toggle ESP32 Board LED.
  - 2-4 Fingers: Sequence control for virtual lights.
  - Full Palm: Turn all lights ON.
  - Closed Fist: Turn all lights OFF.
- **Telegram Bot Integration:** Full remote management including text commands, voice, and remote photography via the board's camera.

---

## 🛠 Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Hardware:** ESP32 (C++/Arduino)
- **Communication:** WebSockets (Real-time data flow)
- **Deployment:** Liara Cloud

---

## 🏗 System Architecture & Challenges

### 1. Real-time Hardware Connectivity (WebSockets)
Connecting the ESP32 to a cloud-based Django server presented two main challenges:
- **Connection Stability:** To prevent the connection from dropping, we implemented a **"Ping-Pong" mechanism**. The board periodically checks the link to ensure it remains active.
- **Command Reliability:** To ensure no instruction was lost during transmission, we utilized a dedicated database layer (Redis/Database-backed queuing) to manage the state and delivery of commands.

> **[PLACEHOLDER: Insert a GIF of the ESP32 reacting to Web commands here]**

### 2. Telegram Bot Proxy Solution
Due to network restrictions on the server side, we couldn't host the Telegram bot directly. 
**Solution:** We developed a local proxy bridge. A local machine connected to a VPN acts as a gateway, routing messages between the Telegram API and our cloud server, ensuring 100% uptime for the bot services.

> **[PLACEHOLDER: Insert a Screenshot of the Telegram Bot interface here]**

---

## 📸 Media & Demos

### Web Interface & Command Line
Description of the UI and the interactive command line.
> **[PLACEHOLDER: Insert a high-res screenshot of your Website's Home Page here]**

### Gesture Control in Action
> **[PLACEHOLDER: Insert a GIF showing you using hand gestures to flip the lights]**

### ESP32 Board Setup
> **[PLACEHOLDER: Insert a photo of your physical hardware setup/wiring here]**

---

## 👥 The Team
This project was a collaborative effort:
- **[Amir's Name]:** Hardware Architecture, ESP32 Programming, and Board-to-Server Integration.
- **Mohammad Jamshidi:** Backend Development, Server Management, and System Logic.
- **Hossein Janghorban:** UI/UX Design and Frontend Development.

---
