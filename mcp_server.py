from mcp.server.fastmcp import FastMCP
import httpx
import os

IDIG_BASE = "https://api.softricks.net/idig"
PORT = int(os.environ.get("PORT", 8000))

mcp = FastMCP(
    "iDig DNS API",
    host="0.0.0.0",   # required by Railway — listen on all interfaces
    port=PORT,         # Railway injects PORT as an environment variable
)

# ── HTTP helper ──────────────────────────────────────────────
async def call_idig(path: str, params: dict) -> dict:
    """Make a real HTTP call to the iDig Lambda API."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{IDIG_BASE}{path}", params=params)
            print(f"iDig API call: {r.url}")
            print(f"iDig API status: {r.status_code}")
            print(f"iDig API response: {r.text}")
            return r.json()
    except Exception as e:
        print(f"iDig API error: {e}")
        raise

# ── Tools ────────────────────────────────────────────────────

@mcp.tool()
async def dns_lookup(domain: str, token: str, rr: str = "a") -> dict:
    """Look up DNS records for a domain. Record types: a, aaaa, ns, mx, txt, soa, caa, srv, cname, ds, tlsa, all."""
    return await call_idig("/", {"d": domain, "rr": rr, "token": token})

@mcp.tool()
async def email_security_audit(domain: str, token: str) -> dict:
    """Full SPF, DKIM, DMARC audit with A-F grade and prioritized fix recommendations."""
    return await call_idig("/email/security", {"d": domain, "token": token})

@mcp.tool()
async def dnssec_validate(domain: str, token: str) -> dict:
    """Validate DNSSEC chain of trust. Returns: secure / insecure / bogus / indeterminate."""
    return await call_idig("/dnssec/validate", {"d": domain, "token": token})

@mcp.tool()
async def dnssec_health(domain: str, token: str) -> dict:
    """DNSSEC health report: key inventory, signature expiry, algorithm assessment, rollover readiness."""
    return await call_idig("/dnssec/health", {"d": domain, "token": token})

@mcp.tool()
async def resolve_check(domain: str, token: str) -> dict:
    """DNS resolution diagnostics. Returns status: ok / nxdomain / nodata / servfail / refused / timeout / degraded."""
    return await call_idig("/resolve/check", {"d": domain, "token": token})

@mcp.tool()
async def diagnose(domain: str, token: str) -> dict:
    """Full diagnosis combining resolution + DNSSEC. Use first when something is broken."""
    return await call_idig("/diagnose", {"d": domain, "token": token})

@mcp.tool()
async def propagation_check(domain: str, token: str, record_type: str = "A") -> dict:
    """Check DNS propagation across 16 global resolvers: Google, Cloudflare, Quad9, China, Korea, Russia."""
    return await call_idig("/propagation", {"d": domain, "t": record_type, "token": token})

@mcp.tool()
async def mx_check(domain: str, token: str) -> dict:
    """MX health + provider detection: Google Workspace, M365, Proofpoint, Zoho, 35+ providers."""
    return await call_idig("/mx/check", {"d": domain, "token": token})

@mcp.tool()
async def domain_status(domain: str, token: str) -> dict:
    """Registrar lock and EPP status. Checks transfer lock, delete lock, serverHold, pendingDelete."""
    return await call_idig("/domain/status", {"d": domain, "token": token})

@mcp.tool()
async def geo_lookup(domain: str, token: str) -> dict:
    """Geolocation and hosting: country, city, ISP, ASN, CDN detection, is_hosting flag."""
    return await call_idig("/geo", {"d": domain, "token": token})

@mcp.tool()
async def ttl_check(domain: str, token: str) -> dict:
    """TTL advisory: flags dangerous TTLs and gives step-by-step migration lowering plan."""
    return await call_idig("/ttl/check", {"d": domain, "token": token})

@mcp.tool()
async def zone_consistency(domain: str, token: str) -> dict:
    """Check all authoritative nameservers return identical answers. Catches lame delegation and SOA mismatches."""
    return await call_idig("/zone/consistency", {"d": domain, "token": token})

@mcp.tool()
async def ssl_check(domain: str, token: str) -> dict:
    """SSL certificate: validity, expiry countdown, domain match, issuer, chain completeness."""
    return await call_idig("/ssl/check", {"d": domain, "token": token})

@mcp.tool()
async def subdomain_discover(domain: str, token: str) -> dict:
    """Discover subdomains by probing 75 common names. Surfaces exposed dev/staging environments."""
    return await call_idig("/subdomains", {"d": domain, "token": token})

if __name__ == "__main__":
    mcp.run(transport="sse")