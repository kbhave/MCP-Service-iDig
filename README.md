# iDig DNS MCP Server

A remote MCP server exposing **14 professional DNS diagnostic tools** from the [iDig API](https://api.softricks.net/idig/docs) — built by Kedar Bhave ( [Softricks](https://softricks.net) ).

Connect any MCP-compatible AI client (Claude Desktop, Cursor, Windsurf, and more) to real DNS infrastructure. Diagnose outages, audit email security, validate DNSSEC, check SSL certificates, trace propagation across 16 global resolvers, and more — all in plain English.

**Live endpoint:** `https://mcp.softricks.net/sse`

---

## Quickstart

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Restart Claude Desktop. You'll see **idig-dns** appear under Connectors.

### Cursor / Windsurf

Add to your MCP settings:

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

### Authentication

All tools require a `token` parameter. Get your token at [api.softricks.net/idig/docs](https://api.softricks.net/idig/docs).

---

## Tools

| Tool | Description |
|---|---|
| `dns_lookup` | Look up any DNS record type: A, AAAA, MX, NS, TXT, SOA, CAA, SRV, CNAME, DS, TLSA |
| `resolve_check` | Resolution diagnostics — returns ok / nxdomain / servfail / timeout / degraded |
| `diagnose` | Full diagnosis combining resolution + DNSSEC — start here when something is broken |
| `email_security_audit` | SPF, DKIM, DMARC audit with A–F grade and prioritized fix recommendations |
| `mx_check` | MX health + provider detection (Google Workspace, M365, Proofpoint, 35+ providers) |
| `dnssec_validate` | DNSSEC chain of trust — returns secure / insecure / bogus / indeterminate |
| `dnssec_health` | Key inventory, signature expiry, algorithm assessment, rollover readiness |
| `propagation_check` | Check propagation across 16 global resolvers: Google, Cloudflare, Quad9, China, Korea, Russia |
| `ssl_check` | Certificate validity, expiry countdown, domain match, issuer, chain completeness |
| `ttl_check` | TTL advisory with step-by-step migration lowering plan |
| `zone_consistency` | Compare all authoritative nameservers — catches lame delegation and SOA mismatches |
| `subdomain_discover` | Probe 75 common subdomains — surfaces exposed dev/staging environments |
| `geo_lookup` | Geolocation, ISP, ASN, CDN detection, hosting flag |
| `domain_status` | EPP registrar lock status — transfer-ready, delete lock, serverHold, pendingDelete |

---

## Example prompts

```
My emails are going to spam for example.com — token is YOUR_TOKEN
```
```
Did my DNS changes propagate yet for example.com? token: YOUR_TOKEN
```
```
Run a full security audit on example.com, token YOUR_TOKEN
```
```
Is the SSL cert for example.com about to expire? token YOUR_TOKEN
```
```
We're migrating example.com to a new host next week — are the TTLs safe? token YOUR_TOKEN
```
```
What subdomains does example.com have exposed? token YOUR_TOKEN
```

---

## Architecture

```
Claude Desktop / Cursor / Windsurf
        │
        │  MCP over SSE
        ▼
mcp.softricks.net          ← Railway (always-on Python/FastMCP server)
        │
        │  HTTPS
        ▼
api.softricks.net/idig     ← AWS Lambda (iDig REST API)
        │
        │  DNS queries
        ▼
Live DNS infrastructure
```

---

## Self-hosting

Clone this repo and deploy your own instance:

```bash
git clone https://github.com/kbhave/MCP-Service-iDig
cd MCP-Service-iDig
pip install -r requirements.txt
python mcp_server.py
```

Or deploy to Railway in one click — connect your GitHub repo and Railway handles the rest.

**Requirements:**
- Python 3.11+
- `mcp==1.26.0`
- `httpx`

---

## Related

- **iDig REST API docs:** https://api.softricks.net/idig/docs
- **DNS Doctor AI Agent:** https://agent.softricks.net
- **iOS App:** https://apps.apple.com/us/app/softricks-idig/id522550738

---

## License

MIT