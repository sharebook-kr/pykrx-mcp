# Render Deployment Guide

## Quick Deploy to Render

This project includes a `render.yaml` blueprint for easy deployment.

### Method 1: One-Click Deploy (Recommended)

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **New +** → **Blueprint**
4. Connect your forked repository
5. Render will automatically detect `render.yaml` and deploy

### Method 2: Manual Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `pykrx-mcp` (or any name you prefer)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install .`
   - **Start Command**: `uvicorn pykrx_mcp.asgi:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` (or upgrade for production)
5. Click **Create Web Service**

## Using the Deployed Server

Once deployed, Render provides a URL like:
```
https://pykrx-mcp.onrender.com
```

### Connect to Claude Desktop

Edit your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pykrx-remote": {
      "url": "https://your-app-name.onrender.com/sse"
    }
  }
}
```

## Local Testing

Test the SSE server locally before deploying:

```bash
# Install dependencies
uv pip install -e .

# Run SSE server
uv run uvicorn pykrx_mcp.asgi:app --host 0.0.0.0 --port 8000

# Test in another terminal
curl http://localhost:8000/sse
```

## Environment Variables

The following environment variables are automatically configured by Render:

- `PORT`: Provided by Render (usually 10000)
- `PYTHON_VERSION`: Set to 3.12 in render.yaml

No additional configuration needed!

## Troubleshooting

### Server not starting
- Check Render logs in the dashboard
- Verify build completed successfully
- Ensure all dependencies installed

### Connection timeout
- Free tier instances sleep after 15 minutes of inactivity
- First request may take ~30 seconds to wake up
- Consider upgrading to paid plan for always-on service

### SSE endpoint not responding
- Verify URL includes `/sse` path: `https://your-app.onrender.com/sse`
- Check firewall/network settings
- Test with `curl` first before connecting Claude Desktop

## Performance Notes

**Free Tier**:
- 750 hours/month
- Sleeps after 15 min inactivity
- Shared CPU/RAM
- Perfect for testing and personal use

**Paid Tiers**:
- Always-on (no sleep)
- Dedicated resources
- Better performance for production workloads
