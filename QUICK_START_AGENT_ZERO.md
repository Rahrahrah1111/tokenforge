# 🚀 Agent Zero Quick Start Guide

## One-Command Setup (Recommended)

Simply run this command in your terminal:

```bash
bash setup_agent_zero_complete.sh
```

You'll be prompted for your password during installation. This script will:
- ✅ Install Docker (if needed)
- ✅ Start Docker service
- ✅ Pull Agent Zero image
- ✅ Start Agent Zero container
- ✅ Verify everything is working

---

## Manual Setup (Step by Step)

If you prefer to do it manually:

### 1. Install Docker

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Important**: After running the last command, **log out and log back in** (or restart) for the docker group change to take effect.

### 2. Verify Docker

```bash
docker --version
docker ps
```

If you get permission errors, either:
- Log out and log back in (recommended)
- Or use `sudo docker` for all commands

### 3. Start Agent Zero

**Option A: Using the startup script (easiest)**
```bash
bash start_agent_zero.sh
```

**Option B: Using Docker Compose**
```bash
docker-compose -f docker-compose.agent-zero.yml up -d
```

**Option C: Direct Docker command**
```bash
docker run -d -p 50001:80 --name agent-zero --restart unless-stopped agent0ai/agent-zero
```

### 4. Configure API Key (Required!)

Agent Zero needs an API key to work. After accessing the web UI:

1. Click the **Settings** icon (⚙️)
2. Add your **OpenRouter API Key** (get free key at https://openrouter.ai/keys)
3. Save settings

See `AGENT_ZERO_API_SETUP.md` for detailed instructions.

### 5. Access Agent Zero

Open your browser and visit: **http://localhost:50001**

---

## Management Commands

| Action | Command |
|--------|---------|
| **Start** | `bash start_agent_zero.sh` |
| **Stop** | `bash stop_agent_zero.sh` |
| **View Logs** | `bash agent_zero_logs.sh` |
| **Check Status** | `docker ps \| grep agent-zero` |
| **Restart** | `bash stop_agent_zero.sh && bash start_agent_zero.sh` |
| **Update** | `docker pull agent0ai/agent-zero:latest && bash stop_agent_zero.sh && bash start_agent_zero.sh` |

---

## What You Get

✅ **Fully configured Agent Zero** running in Docker  
✅ **Web UI** at http://localhost:50001  
✅ **Speech-to-Text** support  
✅ **Text-to-Speech** support  
✅ **Persistent storage** (data survives container restarts)  
✅ **Easy management scripts** for start/stop/logs  

---

## Troubleshooting

### "Permission denied" errors
```bash
# Add yourself to docker group (if not done)
sudo usermod -aG docker $USER

# Then log out and log back in
```

### "Docker daemon not running"
```bash
sudo systemctl start docker
```

### "Port already in use"
```bash
# Check what's using port 50001
sudo lsof -i :50001

# Or change the port in docker-compose.agent-zero.yml
```

### Container won't start
```bash
# Check logs
docker logs agent-zero

# Or if using sudo
sudo docker logs agent-zero
```

---

## Files Created

- `docker-compose.agent-zero.yml` - Docker Compose configuration
- `start_agent_zero.sh` - Start script
- `stop_agent_zero.sh` - Stop script  
- `agent_zero_logs.sh` - Logs viewer
- `setup_agent_zero_complete.sh` - Complete setup script
- `docker_setup.sh` - Docker installation script
- `AGENT_ZERO_SETUP.md` - Full documentation

---

## Next Steps

1. Run `bash setup_agent_zero_complete.sh`
2. Enter your password when prompted
3. Wait for setup to complete
4. Open http://localhost:50001 in your browser
5. Start using Agent Zero! 🎉

---

## Need More Help?

See `AGENT_ZERO_SETUP.md` for complete documentation.

