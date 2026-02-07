<p>
 # 🏠 ESP32-CAM Based Smart Home System
### Final IoT Project

A modern **Internet of Things** smart home dashboard built on **ESP32-CAM** that enables users to control virtual devices and camera features using **natural language commands (text, voice, and image)** supported by artificial intelligence.

This project is developed as a **final project of the Internet of Things (IoT) course**.

--

## 📌 Project Overview

Traditional smart home systems rely on fixed buttons or predefined commands.

This project introduces an **AI-based smart home system** that is capable of understanding **natural language commands in Persian and English** and executing them intelligently.

Users can interact with the system through:
- 🌐 Web Dashboard
- 📝 Text Commands
- 🎙️ Voice Commands
- ✋ Visual/Gesture Commands
- 🤖 Telegram Bot

The system processes commands using a **Large Language Model (LLM)** and translates them into executable actions for the ESP32-CAM and virtual devices.

---

## ✨ Features

- 🌐 **Web-based UI**
- Modern and responsive dashboard
- Command input box
- Device status visualization

- 🧠 **AI command processing**
- Natural language understanding using LLM APIs
- Support for Persian and English commands
- Intelligent command parsing (intent and device extraction)

- 💡 **Virtual lamp control**
- 3 independent virtual lamps
- Visual on/off mode with animations
- Control via AI commands

- 📸 **ESP32-CAM photo capture**
- Capture images from the camera
- Display the last captured image on the dashboard

- 🔦 **Camera flash control**
- Turn on/off the flash using AI commands
- Real-time visual feedback in the user interface

---

### ⭐ Additional features

- 🎙️ **Voice command control**
- Speech-to-text processing
- AI-based command interpretation

- ✋ **Image/Gesture Based Commands**
Hand Gesture Recognition Using Vision AI
- Gesture-to-Action Mapping (e.g. Finger Counting)

- 🤖 **Integration with Telegram Bot**
Control Devices via Telegram Messages
Receive Status Updates and Images

- 📷 **Advanced Camera Settings**
- Image Resolution Control
- Camera Configuration Options

- 🗄️ **Database Integration**
Save Command History
- Save Metadata of Captured Images

- 🖌️ **Advanced UI/UX Design**
- Dark Mode and Light Mode
- Glassmorphism/Soft Shadow Cards
- Smooth Animations and Transitions
- Fully Responsive (Mobile/Tablet/Desktop)

---

## 🧱 System Architecture

The system follows a **Client-Server** architecture:

User Interface (Web / Telegram / Voice / Image)
↓
Python Server (API)
↓
AI Service (LLM / Vision)
↓
ESP32-CAM


### Responsibilities

#### ESP32-CAM
- Camera image capture
- Flash control
- Wi-Fi communication (Station + Access Point modes)

#### Python Server (Production Server)
- API endpoints for commands
- AI request handling
- Device state management
- Database operations

---

## 🧠 AI Command Processing Flow

1. User sends a command (text / voice / image)
2. Command is sent to AI API (LLM)
3. AI extracts structured intent
4.Server executes the corresponding action
5.UI updates in real time

## 🛠️ Technology Stack

Hardware
ESP32-CAM

Backend
Python (ِDjango / FastAPI)
RESTful APIs
Hosted on a real online server

Frontend
HTML, CSS, JavaScript
Responsive dashboard UI
Animations & visual feedback

AI Services
Large Language Model (LLM)
Speech-to-Text API
Vision AI for gesture recognition

Database
Used for storing:
Commands history
Images metadata
Device states

## 🌍 Deployment
✅ The project is fully deployed on a real server

✅ No local-only implementation

✅ Accessible via web browser

✅ Suitable for real-world demonstration

🎯 Educational Value
This project demonstrates:

Practical IoT system design
AI integration in embedded systems
Real-world client–server architecture
Modern web UI/UX design
Cloud deployment experience

✅ Conclusion
This project is a complete, production-level IoT Smart Home System that successfully combines:

Embedded systems
Artificial Intelligence
Web technologies
Cloud deployment
It  is designed to be scalable, modern, and user-friendly.

⭐ Thank you for reviewing this project.
     
</p>

