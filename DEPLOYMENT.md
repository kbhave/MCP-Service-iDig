# iDig MCP Server — Railway Deployment Guide

## Project structure
```
idig-mcp/
├── mcp_server.py      ← the MCP server
├── requirements.txt   ← mcp + httpx
└── Procfile           ← tells Railway how to start it
```
That's it. Three files. No Dockerfile needed — Railway detects Python automatically.

---

## Step 1 — Create a GitHub repository

1. Go to https://github.com and click **New repository**
2. Name it `idig-mcp`
3. Make it **Private** (your token handling logic is in here)
4. Click **Create repository**

Then on your Mac, open Terminal:
```bash
# Create the project folder
mkdir ~/idig-mcp
cd ~/idig-mcp

# Copy the 3 files into this folder
# (mcp_server.py, requirements.txt, Procfile)

# Initialize git and push
git init
git add .
git commit -m "Initial iDig MCP server"
git remote add origin https://github.com/YOURNAME/idig-mcp.git
git push -u origin main
```

---

## Step 2 — Create a Railway account

1. Go to https://railway.app
2. Click **Login with GitHub** — use the same GitHub account
3. Authorize Railway when prompted
4. You land on the Railway dashboard

---

## Step 3 — Deploy from GitHub

1. Click **New Project**
2. Click **Deploy from GitHub repo**
3. Select your `idig-mcp` repository
4. Click **Deploy Now**

Railway detects Python automatically, installs your `requirements.txt`,
and runs the `Procfile` command. You'll see live build logs.

The build takes about 60 seconds. When done you'll see a green **Active** status.

---

## Step 4 — Get your Railway URL

1. Click on your deployed service
2. Go to **Settings → Networking**
3. Click **Generate Domain**
4. Railway gives you a URL like: `idig-mcp.up.railway.app`

Test it immediately:
```bash
curl https://idig-mcp.up.railway.app
```
You should get a response — even an error message confirms the server is running.

---

## Step 5 — Point mcp.softricks.net to Railway

Since `softricks.net` is registered in Squarespace, you'll add the DNS record there:

1. Log into **Squarespace → Domains → softricks.net → DNS Settings**
2. Add a new record:
   - **Type:** CNAME
   - **Host:** mcp
   - **Value:** idig-mcp.up.railway.app
   - **TTL:** 3600

3. Back in Railway → **Settings → Networking → Custom Domain**
4. Enter: `mcp.softricks.net`
5. Railway verifies the CNAME and issues an SSL certificate automatically

Wait 5–10 minutes for DNS to propagate, then test:
```bash
curl https://mcp.softricks.net
```

---

## Step 6 — Connect Claude Desktop

Install Claude Desktop: https://claude.ai/download

Edit the config file on your Mac:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Open it in any text editor (TextEdit, VS Code, etc.) and add:
```json
{
  "mcpServers": {
    "idig-dns": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.softricks.net/sse"
      ]
    }
  }
}
```

If the file doesn't exist yet, create it with exactly that content.

Restart Claude Desktop completely (Cmd+Q, then reopen).

---

## Step 7 — Verify tools are registered

After restarting Claude Desktop:
1. Look for a **🔧 tools icon** in the chat input area
2. Click it — you should see all 14 iDig tools listed:
   - dns_lookup
   - email_security_audit
   - dnssec_validate
   - dnssec_health
   - resolve_check
   - diagnose
   - propagation_check
   - mx_check
   - domain_status
   - geo_lookup
   - ttl_check
   - zone_consistency
   - ssl_check
   - subdomain_discover

---

## Step 8 — Test a tool call

Type this in Claude Desktop:
```
Check the DNSSEC status of secure64.com  — my token is YOUR_TOKEN_HERE
```

Claude should call `dnssec_validate`, hit your Lambda API, and return a real result.

---

## Making changes going forward

Every time you update `mcp_server.py`:
```bash
cd ~/idig-mcp
git add .
git commit -m "describe your change"
git push
```
Railway detects the push and auto-redeploys. Takes about 60 seconds.
No manual steps needed — same workflow as Netlify.

---

## Troubleshooting

**Build fails on Railway:**
Check the build logs in Railway dashboard. Most common cause:
a package in `requirements.txt` can't be found. Try pinning versions:
```
mcp==1.3.0
httpx==0.27.0
```

**Tools not showing in Claude Desktop:**
- Confirm the URL ends in `/sse`: `https://mcp.softricks.net/sse`
- Check Claude Desktop logs on Mac: `~/Library/Logs/Claude/`
- Make sure you fully quit and restarted Claude Desktop (Cmd+Q)

**"Connection refused" from curl:**
The app crashed on startup. Check Railway logs:
Railway dashboard → your service → **Deployments** → click the deployment → **View Logs**

**Token errors from iDig API:**
The token is passed per tool call. Make sure your iDig API CORS policy
allows requests from Railway's IP range — or set `allow_origins=["*"]`
since these are server-to-server calls with no browser involved.

---

## Architecture — final picture

```
Claude Desktop / Cursor / Windsurf / any MCP client
              │
              │  MCP over SSE
              ▼
  mcp.softricks.net          ← Railway, always-on, auto-restarts
  (mcp_server.py)
              │
              │  HTTPS GET requests
              ▼
  api.softricks.net/idig     ← AWS Lambda, unchanged
  (your existing API)
```
