# 📡 ESP32 Distance Monitoring System

A full-stack IoT monitoring platform that captures distance readings from an ESP32 micro-controller sensor, processes them via a Django REST API, and delivers analytical reports through an interactive Telegram Bot.

---

## 🛠 Tech Stack

* **Hardware:** ESP32 DevKit v1, TOFO50C (VL6180X distance sensor)
* **Backend:** Python 3.12, Django, Django REST Framework
* **Database:** PostgreSQL 16
* **Telegram Bot:** `python-telegram-bot`, `httpx`
* **DevOps & Monitoring:** Docker, Docker Compose, Dockmon

---

## 🚀 Key Features

* **Real-time Sensor Ingestion:** HTTP POST endpoints accepting distance telemetry from ESP32.
* **REST API:** Handles data persistence, authentication, and report exports.
* **Telegram Bot Integration:** Requests live metrics and generates downloadable CSV/chart reports.
* **Containerized Architecture:** Fully dockerized services (`db`, `web`, `bot`, `dockmon`) isolated with tiered monitoring labels.

---

## 🏁 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/danielshevchenko03-cmd/esp32-distance-monitor.git](https://github.com/danielshevchenko03-cmd/esp32-distance-monitor.git)
   cd esp32-distance-monitor
   ```
2. Configure environment variables:
Copy .env.example to .env and populate your secrets:

```bash
cp .env.example .env
```

3. Launch with Docker Compose:

```bash
docker compose up -d --build
```

4. Access services:

Django API: http://localhost:8000

Dockmon Dashboard: http://localhost:8001