# Agent-Zero Docker Installation Guide (Zorin Linux)

## Quick Installation Steps

### Step 1: Install Docker
Open a terminal and run:
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 2: Add your user to docker group (optional, but recommended)
This allows you to run Docker without `sudo`:
```bash
sudo usermod -aG docker $USER
```
**Important**: After this command, you need to **log out and log back in** (or restart) for the change to take effect.

Alternatively, you can use `newgrp docker` in your current terminal session, or just use `sudo` with all docker commands.

### Step 3: Pull and run Agent-Zero
```bash
docker pull agent0ai/agent-zero
docker run -p 50001:80 agent0ai/agent-zero
```

If you didn't log out/log in after Step 2, use:
```bash
sudo docker pull agent0ai/agent-zero
sudo docker run -p 50001:80 agent0ai/agent-zero
```

### Step 4: Access the application
Open your browser and visit: **http://localhost:50001**

The container will run in the foreground. Press `Ctrl+C` to stop it.

## Running in Background (Optional)
To run the container in the background:
```bash
docker run -d -p 50001:80 --name agent-zero agent0ai/agent-zero
```

To stop it later:
```bash
docker stop agent-zero
```

To start it again:
```bash
docker start agent-zero
```

