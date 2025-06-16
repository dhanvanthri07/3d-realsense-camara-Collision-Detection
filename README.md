# 🛡️ RealSense + ESP32 Collision Detection System

A real-time 3D collision detection system using Intel® RealSense™, OpenCV, and an ESP32-based IIoT controller. Designed for automation, robotics, and industrial safety applications.

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

| Component               | Description                         |
|------------------------|-------------------------------------|
| 🎥 RealSense D435i     | Depth-sensing 3D camera             |
| 🔌 ESP32 (NORVI IIoT)  | Microcontroller with serial support |
| 💡 LED / Motor Driver  | Optional output indicator           |
| 🧠 Host Computer        | Running Python 3.8+, OpenCV, etc.   |

---

## 🎥 Demo

Here’s how the RealSense collision detection with ESP32 works:

![Demo](https://github.com/user-attachments/assets/cdcb8fdb-0f49-49eb-b9fd-ba0ed2f0db03)

---

## ⚙️ Installation

### 1. Install Python Dependencies

```bash
pip install pyrealsense2 opencv-python pyserial numpy

