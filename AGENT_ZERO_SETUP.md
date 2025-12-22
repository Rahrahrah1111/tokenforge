# Agent Zero Complete Setup Guide

This guide will help you set up Agent Zero AI framework completely on Zorin Linux.

## What is Agent Zero?

Agent Zero is a fully dockerized AI framework with:
- 🤖 Autonomous AI agent capabilities
- 🎤 Speech-to-Text (STT) integration
- 🔊 Text-to-Speech (TTS) integration
- 🌐 Web UI accessible at http://localhost:50001
- 🧠 Memory and knowledge management
- 🔧 Extensible tool system

**GitHub**: https://github.com/agent0ai/agent-zero

---

## Quick Setup (Automated)

### Step 1: Install Docker

Run the automated setup script:

```bash
bash docker_setup.sh
```

This will:
- Install Docker if not already installed
- Start Docker service
- Add your user to docker group (requires logout/login)
- Pull the Agent Zero image
- Start the container

**Note**: After adding yourself to the docker group, you need to **log out and log back in** for changes to take effect.

---

## Manual Setup

### Step 1: Install Docker

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Important**: Log out and log back in after adding yourself to the docker group.

### Step 2: Verify Docker Installation

```bash
docker --version
docker ps
```

### Step 3: Pull Agent Zero Image

```bash
docker pull agent0ai/agent-zero:latest
```

### Step 4: Start Agent Zero

**Option A: Using Docker Compose (Recommended)**

```bash
bash start_agent_zero.sh
```

**Option B: Using Docker directly**

```bash
docker run -d -p 50001:80 --name agent-zero --restart unless-stopped agent0ai/agent-zero
```

**Option C: Using Docker Compose manually**

```bash
docker-compose -f docker-compose.agent-zero.yml up -d
```

---

## Management Commands

### Start Agent Zero
```bash
bash start_agent_zero.sh
```

### Stop Agent Zero
```bash
bash stop_agent_zero.sh
```

### View Logs
```bash
bash agent_zero_logs.sh
# or
docker logs -f agent-zero
```

### Check Status
```bash
docker ps | grep agent-zero
```

### Restart Agent Zero
```bash
bash stop_agent_zero.sh
bash start_agent_zero.sh
```

### Update to Latest Version
```bash
docker pull agent0ai/agent-zero:latest
bash stop_agent_zero.sh
bash start_agent_zero.sh
```

---

## Accessing Agent Zero

Once running, open your browser and visit:

**http://localhost:50001**

The web UI provides:
- Chat interface with the AI agent
- Speech-to-Text input
- Text-to-Speech output
- Settings and configuration
- Memory management
- Project management

---

## Features

### Speech-to-Text (STT)
- Click the microphone icon in the web UI
- Speak your commands/questions
- Agent Zero will transcribe and process them

### Text-to-Speech (TTS)
- Agent responses can be read aloud
- Configure in the Settings page

### Memory System
- Agent Zero remembers conversations
- Access memory dashboard in the UI
- Persistent storage across sessions

### Projects
- Organize conversations into projects
- Custom instructions per project
- Project-specific secrets and configuration

---

## Configuration

### Environment Variables

You can modify `docker-compose.agent-zero.yml` to add environment variables:

```yaml
environment:
  - CUSTOM_VAR=value
```

### Persistent Data

Data is automatically persisted in Docker volumes:
- `agent-zero-data`: Application data
- `agent-zero-logs`: Log files
- `agent-zero-memory`: Memory storage
- `agent-zero-knowledge`: Knowledge base

### Port Configuration

To change the port, edit `docker-compose.agent-zero.yml`:

```yaml
ports:
  - "YOUR_PORT:80"  # Change YOUR_PORT to desired port
```

---

## Troubleshooting

### Docker Permission Denied

If you get permission errors:
```bash
sudo usermod -aG docker $USER
# Then log out and log back in
```

Or use `sudo` with docker commands temporarily.

### Container Won't Start

Check logs:
```bash
docker logs agent-zero
```

Check if port is already in use:
```bash
sudo lsof -i :50001
```

### Can't Access Web UI

1. Verify container is running: `docker ps | grep agent-zero`
2. Check if port is correct: `docker port agent-zero`
3. Try accessing from another browser or incognito mode
4. Check firewall settings

### Update Issues

If update fails:
```bash
docker stop agent-zero
docker rm agent-zero
docker pull agent0ai/agent-zero:latest
bash start_agent_zero.sh
```

---

## Advanced Usage

### Run in Foreground (for debugging)

```bash
docker run -p 50001:80 agent0ai/agent-zero
```

### Access Container Shell

```bash
docker exec -it agent-zero /bin/bash
```

### View Container Resources

```bash
docker stats agent-zero
```

### Backup Data

```bash
docker run --rm -v agent-zero-data:/data -v $(pwd):/backup alpine tar czf /backup/agent-zero-backup.tar.gz -C /data .
```

### Restore Data

```bash
docker run --rm -v agent-zero-data:/data -v $(pwd):/backup alpine tar xzf /backup/agent-zero-backup.tar.gz -C /data
```

---

## Security Notes

⚠️ **Important**: Agent Zero can be powerful and potentially dangerous if misconfigured. Always:
- Run in isolated Docker environment (which we're doing)
- Be careful with system prompts and instructions
- Review what the agent is doing
- Don't give it access to sensitive credentials unless necessary

---

## Documentation

For more information, visit:
- **GitHub**: https://github.com/agent0ai/agent-zero
- **Documentation**: Check the `/docs` folder in the repository
- **Issues**: https://github.com/agent0ai/agent-zero/issues

---

## Support

- **Discord**: Join the Agent Zero Discord community
- **GitHub Issues**: Report bugs and request features
- **YouTube**: Watch tutorials and demos

---

## Next Steps

1. ✅ Docker installed
2. ✅ Agent Zero running
3. 🌐 Open http://localhost:50001
4. 🔑 **Configure API Key** (Required - see AGENT_ZERO_API_SETUP.md)
5. 🎤 Try the Speech-to-Text feature
6. 🔊 Enable Text-to-Speech
7. 🧠 Explore the memory system
8. 📁 Create your first project

**⚠️ Important**: Agent Zero requires an API key to work. See `AGENT_ZERO_API_SETUP.md` for setup instructions.

**Enjoy using Agent Zero!** 🚀

