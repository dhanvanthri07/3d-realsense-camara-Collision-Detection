# 🛡️ RealSense + ESP32 Collision Detection System

A real-time 3D collision detection system using Intel® RealSense™, OpenCV, and an ESP32-based IIoT controller. Designed for automation, robotics, and industrial safety applications.

(![demo gif-ezgif com-animated-gif-maker](https://github.com/user-attachments/assets/18889d6c-d605-4d19-a47a-eefbb41eca1f)
)

---

## 📚 Table of Contents
- [Overview](#-overview)
- [Hardware Requirements](#-hardware-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [System Architecture](#-system-architecture)
- [Serial Communication Protocol](#-serial-communication-protocol)
- [Demo](#-demo)
- [License](#-license)

---

## 🚀 Overview

This project connects an Intel RealSense depth camera with an ESP32 over serial communication. If an object is detected within a **2-meter range**, a warning signal is sent to trigger external systems such as alarms, lights, or motors.

> 💡 Includes visual feedback with OpenCV and depth-based safety logic.

---

## 🛠️ Hardware Requirements

| Component               | Description                        |
|------------------------|------------------------------------|
| 🎥 RealSense D435i     | Depth-sensing camera               |
| 🔌 ESP32 (NORVI IIoT)  | Microcontroller with serial support |
| 💡 LED / Motor Driver  | Optional output indicator          |
| 🧠 Computer             | Running Python 3.8+ & OpenCV       |

---

## 🎥 Demo

Here’s how the RealSense collision detection with ESP32 works:

![Demo](![demo-ezgif com-split](https://github.com/user-attachments/assets/d8b4e459-ffa1-437b-b22b-955388b1d78a)
)
)


## ⚙️ Installation

### 1. Python Dependencies
```bash
pip install pyrealsense2 opencv-python pyserial numpy


