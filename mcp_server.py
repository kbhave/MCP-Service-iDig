from mcp.server.fastmcp import FastMCP
import httpx
import os

IDIG_BASE = "https://api.softricks.net/idig"
PORT = int(os.environ.get("PORT", 8080))

mcp = FastMCP(
    "iDig DNS API",
    host="0.0.0.0",
    port=PORT,
)

async def call_idig(path: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{IDIG_BASE}{path}", params=params)
        print(f"URL: {r.url} STATUS: {r.status_code}", flush=True)
        return r.json()

@mcp.tool()
async def dns_lookup(domain: str, token: str, rr: str = "a") -> dict:
    """Look up DNS records for a domain. Record types: a, aaaa, ns, mx, txt, soa, caa, srv, cname, ds, tlsa, https, svcb, any, all."""
    return await call_idig("/", {"d": domain, "rr": rr, "token": token})

@mcp.tool()
async def email_security_audit(domain: str, token: str) -> dict:
    """Full SPF, DKIM, DMARC, and BIMI audit with A-F grade and prioritized fix recommendations."""
    return await call_idig("/email/security", {"d": domain, "token": token})

@mcp.tool()
async def dnssec_validate(domain: str, token: str) -> dict:
    """Validate DNSSEC chain of trust. Returns: secure / insecure / bogus / indeterminate."""
    return await call_idig("/dnssec/validate", {"d": domain, "token": token})

@mcp.tool()
async def dnssec_health(domain: str, token: str) -> dict:
    """DNSSEC health report: key inventory, signature expiry, algorithm assessment, DS at parent, rollover readiness, full chain of trust (Root → TLD → Domain) with chain_intact flag and broken-link identification, warnings, and recommendations."""
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
    """Discover subdomains by probing 75 common names plus crt.sh Certificate Transparency logs. Surfaces exposed dev/staging environments."""
    return await call_idig("/subdomains", {"d": domain, "token": token})

@mcp.tool()
async def blacklist_check(domain: str, token: str) -> dict:
    """IP blacklist / DNSBL check. Tests A-record and MX IPs against Spamhaus, Barracuda, SpamCop, SORBS, and more."""
    return await call_idig("/blacklist/check", {"d": domain, "token": token})

@mcp.tool()
async def whois_lookup(domain: str, token: str) -> dict:
    """Parsed WHOIS: registrar, creation/expiry dates, domain age, nameservers, EPP status, DNSSEC status."""
    return await call_idig("/whois", {"d": domain, "token": token})

@mcp.tool()
async def http_check(domain: str, token: str) -> dict:
    """HTTP/HTTPS reachability: status codes, redirect chain, HSTS header, HTTP→HTTPS redirect detection."""
    return await call_idig("/http/check", {"d": domain, "token": token})

@mcp.tool()
async def zone_axfr(domain: str, token: str) -> dict:
    """AXFR zone transfer vulnerability check. Tests whether any authoritative NS allows public zone transfers (critical misconfiguration)."""
    return await call_idig("/zone/axfr", {"d": domain, "token": token})

@mcp.tool()
async def dane_validate(domain: str, token: str, port: int = 443) -> dict:
    """DANE/TLSA validation: cross-validates TLSA DNS records against the live TLS certificate. Supports all four TLSA usage types."""
    return await call_idig("/dane/validate", {"d": domain, "token": token, "port": port})

if __name__ == "__main__":
    mcp.run(transport="sse")