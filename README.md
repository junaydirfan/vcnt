# vcnt - Discord Voice Logger Bot

A lightweight Discord bot that logs voice channel join, leave, and move events, and provides a simple `/coin` slash command for a coin flip. Built with Python and discord.py, and deployed on a Proxmox home server with systemd for 24/7 availability.

---

## Features

* **Voice State Logging**: Logs when users join, leave, or switch voice channels.
* **Slash Command**: `/coin` flips a coin and returns **Heads** or **Tails**.
* **Configurable** via environment variables in a `.env` file.
* **Systemd Service**: Runs continuously under systemd on a Proxmox VM or container.

---

## Prerequisites

* A Discord Developer Application with the following enabled under **Privileged Gateway Intents**:

  * **Voice State Intent** (required for voice logging)
  * **Server Members Intent** (optional)
  * **Message Content Intent** (optional)
* **OAuth2 Scopes**:

  * `bot`, `applications.commands` (for slash commands)
* A Proxmox VE host with a Debian or Ubuntu VM/LXC (1–2 GB RAM, internet access).
* Python 3.10+ installed on the host.

---

## Repository Structure

```
vcnt/                  # Project root
├── bot.py             # Main bot code (voice logging + slash commands)
├── requirements.txt   # Python dependencies
├── .gitignore         # Ignored files & folders
└── README.md          # This documentation
```

---

## Installation

1. **Clone the repository**:

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

Create a `.env` file in the project root (do not commit to Git):

```dotenv
DISCORD_TOKEN=<YOUR_BOT_TOKEN>
LOG_CHANNEL_ID=<TEXT_CHANNEL_ID>
APPLICATION_ID=<YOUR_APPLICATION_ID>
GUILD_ID=<YOUR_TEST_GUILD_ID>
```

* **DISCORD\_TOKEN**: Your bot’s token (rotate if exposed).
* **LOG\_CHANNEL\_ID**: ID of the channel to log voice events.
* **APPLICATION\_ID**: Your App’s Client ID (from Developer Portal).
* **GUILD\_ID**: (For testing) your server’s ID to register slash commands instantly.

Slash commands require the `applications.commands` scope and proper OAuth2 invite.

---

## Running Locally

1. **Activate** the virtual environment:

   ```bash
   source venv/bin/activate
   ```
2. **Start** the bot:

   ```bash
   python bot.py
   ```
3. In your test server:

   * Type `/coin` to flip a coin immediately.
   * Join/leave voice channels to see log messages sent to the configured channel.

---

## Deployment on Proxmox

1. **Create** a Debian/Ubuntu VM or LXC in Proxmox.
2. **SSH into the guest**:

   ```bash
   ssh root@<VM_IP>
   ```
3. **Install prerequisites**:

   ```bash
   apt update && apt install -y python3 python3-venv python3-pip git
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
   deactivate
   ```
5. **Create the `.env`** under `/opt/vcnt` (same entries as above) and `chmod 600 .env`.
6. **Create a systemd service** at `/etc/systemd/system/vcnt.service`:

   ```ini
   [Unit]
   Description=vcnt Discord Bot (Voice Logger + /coin)
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
   journalctl -u vcnt -f
   ```

---

## Updating the Bot

After making changes and pushing to GitHub:

```bash
ssh root@<VM_IP>
cd /opt/vcnt
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # if new deps
systemctl restart vcnt
journalctl -u vcnt -f
```

---

## License

MIT License. Feel free to use and modify!
