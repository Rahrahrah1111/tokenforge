# Agent Zero Troubleshooting Guide

## Common Errors and Solutions

---

## Error 1: 401 Unauthorized

**Error Message:**
```
AuthenticationError: OpenrouterException - {"error":{"message":"No cookie auth credentials found","code":401}}
```

**Solution:**
- You need to add an API key
- See: `FIX_API_ERROR.md` or `AGENT_ZERO_API_SETUP.md`

---

## Error 2: 402 Payment Required / Credits Error

**Error Message:**
```
APIError: This request requires more credits, or fewer max_tokens. 
You requested up to 64000 tokens, but can only afford 4717.
```

**Solution:**
- Switch to a **free model** in Agent Zero Settings
- Or reduce max_tokens to 4000
- See: `FIX_CREDITS_ERROR.md` for detailed steps

**Quick Fix:**
1. Open Settings (⚙️)
2. Change model to: `meta-llama/llama-3.2-3b-instruct:free`
3. Save and try again

---

## Error 3: Container Won't Start

**Symptoms:**
- `docker ps` shows no agent-zero container
- Error when running `start_agent_zero.sh`

**Solutions:**

1. **Check Docker is running:**
   ```bash
   sudo systemctl status docker
   ```
   If not running:
   ```bash
   sudo systemctl start docker
   ```

2. **Check port is available:**
   ```bash
   sudo lsof -i :50001
   ```
   If something is using it, either:
   - Stop that service, OR
   - Change port in `docker-compose.agent-zero.yml`

3. **Check logs:**
   ```bash
   docker logs agent-zero
   ```

4. **Remove old container and restart:**
   ```bash
   docker stop agent-zero
   docker rm agent-zero
   bash start_agent_zero.sh
   ```

---

## Error 4: Can't Access Web UI

**Symptoms:**
- Browser shows "Connection refused" or timeout
- http://localhost:50001 doesn't load

**Solutions:**

1. **Verify container is running:**
   ```bash
   docker ps | grep agent-zero
   ```

2. **Check port mapping:**
   ```bash
   docker port agent-zero
   ```
   Should show: `80/tcp -> 0.0.0.0:50001`

3. **Check firewall:**
   ```bash
   sudo ufw status
   ```
   If firewall is active, allow port 50001:
   ```bash
   sudo ufw allow 50001
   ```

4. **Try from container IP:**
   ```bash
   docker inspect agent-zero | grep IPAddress
   ```
   Then try: `http://<container-ip>:80`

5. **Check browser console** (F12) for errors

---

## Error 5: Settings Not Saving

**Symptoms:**
- Changes in Settings don't persist
- API keys disappear after refresh

**Solutions:**

1. **Check browser storage:**
   - Open browser console (F12)
   - Check if localStorage is enabled
   - Try incognito/private mode

2. **Check Docker volumes:**
   ```bash
   docker volume ls | grep agent-zero
   ```
   Volumes should exist for data persistence

3. **Restart container:**
   ```bash
   bash stop_agent_zero.sh
   bash start_agent_zero.sh
   ```

---

## Error 6: Model Not Responding

**Symptoms:**
- Messages sent but no response
- "Generating..." but never completes

**Solutions:**

1. **Check model is free/affordable:**
   - Switch to a free model
   - See `FIX_CREDITS_ERROR.md`

2. **Check API key is valid:**
   - Verify key at provider dashboard
   - Try regenerating key

3. **Reduce max_tokens:**
   - Lower to 2000-4000 in Settings

4. **Check logs:**
   ```bash
   bash agent_zero_logs.sh
   ```
   Look for specific error messages

---

## Error 7: Speech-to-Text Not Working

**Symptoms:**
- Microphone button doesn't work
- No audio input detected

**Solutions:**

1. **Check browser permissions:**
   - Browser must allow microphone access
   - Check browser settings

2. **Check HTTPS requirement:**
   - Some browsers require HTTPS for microphone
   - Try accessing via: `https://localhost:50001` (if configured)

3. **Check audio device:**
   - Verify microphone works in other apps
   - Check system audio settings

---

## Error 8: Text-to-Speech Not Working

**Symptoms:**
- No audio output
- TTS option grayed out

**Solutions:**

1. **Enable TTS in Settings:**
   - Check TTS is enabled
   - Select a TTS provider

2. **Check browser audio:**
   - Verify system volume is up
   - Check browser isn't muted

3. **Check TTS provider:**
   - Some providers need API keys
   - Configure in Settings

---

## General Troubleshooting Steps

### 1. Check Container Status
```bash
docker ps -a | grep agent-zero
```

### 2. View Logs
```bash
bash agent_zero_logs.sh
# or
docker logs -f agent-zero
```

### 3. Restart Container
```bash
bash stop_agent_zero.sh
bash start_agent_zero.sh
```

### 4. Update to Latest Version
```bash
docker pull agent0ai/agent-zero:latest
bash stop_agent_zero.sh
bash start_agent_zero.sh
```

### 5. Check System Resources
```bash
docker stats agent-zero
```

### 6. Check Docker System
```bash
docker system df
docker system prune  # Clean up if needed (be careful!)
```

---

## Getting More Help

1. **Check Agent Zero logs:**
   ```bash
   bash agent_zero_logs.sh
   ```

2. **Check Agent Zero documentation:**
   - GitHub: https://github.com/agent0ai/agent-zero
   - Docs: Check `/docs` folder in repository

3. **Check provider status:**
   - OpenRouter: https://openrouter.ai/status
   - Google AI: Check Google Cloud status

4. **GitHub Issues:**
   - https://github.com/agent0ai/agent-zero/issues
   - Search for similar issues
   - Create new issue if needed

---

## Quick Reference

| Error Code | Meaning | Quick Fix |
|------------|---------|-----------|
| 401 | No API key | Add API key in Settings |
| 402 | Not enough credits | Switch to free model |
| 403 | Forbidden | Check API key permissions |
| 429 | Rate limited | Wait or upgrade plan |
| 500 | Server error | Check provider status |

---

## Prevention Tips

1. ✅ **Always use free models** when starting out
2. ✅ **Set reasonable max_tokens** (2000-4000)
3. ✅ **Monitor your usage** in provider dashboard
4. ✅ **Keep API keys secure** - never share publicly
5. ✅ **Update regularly** - `docker pull agent0ai/agent-zero:latest`

---

**Still having issues?** Check the specific error guide or Agent Zero GitHub issues.






