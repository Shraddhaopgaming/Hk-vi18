# 🚀 HK-vi18 VPS Management Bot

## Made by AryanDev | Discord ID: devaru007

### 📋 Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Commands](#commands)
- [Docker Images](#docker-images)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## ✨ Features

- **Multiple OS Support**: Ubuntu, Debian, Alpine, Arch, Kali, Fedora, CentOS, Rocky Linux
- **Interactive UI**: Beautiful Discord embeds with buttons for easy management
- **Resource Monitoring**: Real-time CPU, RAM, Disk usage tracking
- **SSH Access**: Automatic tmate SSH session generation
- **VPS Management**: Start, Stop, Restart, Remove VPS instances
- **Node Statistics**: System resource monitoring
- **Admin Commands**: Full administrative control
- **Docker Integration**: Custom Docker images for each OS
- **Database Storage**: Persistent VPS tracking
- **Logging System**: Comprehensive activity logs

---

## 📦 Prerequisites

### System Requirements
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- 4GB+ RAM (8GB recommended)
- 20GB+ free disk space
- Docker installed
- Python 3.8+
- Discord Bot Token
- ===
- Cmd Run
- ===
- # Create service file
sudo nano /etc/systemd/system/vps-bot.service

[Unit]
Description=VPS Management Bot
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/vps-bot
ExecStart=/usr/bin/python3 /home/ubuntu/vps-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

### Install Docker
```bash
# For Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
```docker --version```
