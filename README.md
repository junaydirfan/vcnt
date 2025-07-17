# vcnt - Discord Voice Logger Bot

A lightweight Discord bot that logs voice channel join, leave, and move events to a designated text channel (or direct messages). Built with Python and discord.py, and deployed on a Proxmox home server with systemd for 24/7 availability.

---

## Features

* Logs when users join, leave, or switch voice channels.
* Sends formatted messages to a specified Discord text channel.
* Configurable via environment variables (`.env`).
* Runs continuously under systemd on a Proxmox VM or container.

---

## Prerequisites

* Discord bot application with **Voice State Intent** (and optional **Server Members Intent** and **Message Content Intent**).
* Proxmox VE with a Debian or Ubuntu VM/LXC (1–2 GB RAM, internet access).
* Host machine or VM with internet access for Discord API (port 443).

---

## Repository Structure

```
vcnt/                  # Project root
├── bot.py             # Main bot code
├── requirements.txt   # Python dependencies
├── .gitignore         # Ignored files & folders
└── README.md          # This file
```

---

## Installation

1. **Clone the repository** on your local machine:

   ```bash
   git clone https://github.com/<YourUsername>/vcnt.git
   cd vcnt
   ```
2. **Create a virtual environment** and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the project root (never commit this to Git):

```env
DISCORD_TOKEN=<YOUR_BOT_TOKEN>
LOG_CHANNEL_ID=<TEXT_CHANNEL_ID>
```

* **DISCORD\_TOKEN**: Your bot’s token (rotate if exposed).
* **LOG\_CHANNEL\_ID**: The ID of the text channel where events will be logged.

Load them in `bot.py` via `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
```

---

## Running Locally

Start the bot for testing on your PC:

```bash
source venv/bin/activate
python bot.py
```

Join/leave voice channels in your test server to verify logs.

---

## Deployment on Proxmox

1. **Create a VM or LXC** (Debian/Ubuntu) via Proxmox GUI.
2. **SSH into the guest**:

   ```bash
   ssh root@<VM_IP>
   ```
3. **Install system packages**:

   ```bash
   apt update
   apt install -y python3 python3-venv python3-pip git
   ```
4. **Clone and set up**:

   ```bash
   cd /opt
   git clone https://github.com/<YourUsername>/vcnt.git
   cd vcnt
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Create the `.env`** under `/opt/vcnt`:

   ```bash
   cat > .env <<EOF
   DISCORD_TOKEN=<YOUR_BOT_TOKEN>
   LOG_CHANNEL_ID=<TEXT_CHANNEL_ID>
   EOF
   chmod 600 .env
   ```
6. **Set up systemd service** `/etc/systemd/system/vcnt.service`:

   ```ini
   [Unit]
   Description=vcnt Discord Voice Logger Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/opt/vcnt
   EnvironmentFile=/opt/vcnt/.env
   ExecStart=/opt/vcnt/venv/bin/python bot.py
   Restart=on-failure
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
7. **Enable & start**:

   ```bash
   systemctl daemon-reload
   systemctl enable vcnt
   systemctl start vcnt
   ```
8. **Verify logs**:

   ```bash
   systemctl status vcnt
   journalctl -u vcnt -f
   ```

---

## Updating the Bot

Whenever you push changes to GitHub:

```bash
ssh root@<VM_IP>
cd /opt/vcnt
git pull
source venv/bin/activate
pip install -r requirements.txt  # if new dependencies
systemctl restart vcnt
journalctl -u vcnt -f
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is released under the MIT License.
