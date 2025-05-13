import asyncio
from urllib.parse import urlparse, urlunparse
import httpx
from collections import defaultdict, deque
import time


# Track timestamps of requests per domain
request_history: dict[str, deque] = defaultdict(lambda: deque(maxlen=10))

async def get_webpage(url: str) -> httpx.Response:
    MAX_REQUESTS_PER_MINUTE = 3
    base_domain = get_base_domain(url)

    now = time.time()
    timestamps = request_history[base_domain]

    # Remove timestamps older than 60 seconds
    while timestamps and now - timestamps[0] > 60:
        timestamps.popleft()

    if len(timestamps) >= MAX_REQUESTS_PER_MINUTE:
        wait_time = 60 - (now - timestamps[0])
        print(f"[{base_domain}] Throttle hit. Sleeping {wait_time:.1f}s...")
        await asyncio.sleep(wait_time)

    # Record this request
    timestamps.append(time.time())

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
    return response

def strip_url(url: str) -> str:
    parsed = urlparse(url)
    stripped = parsed._replace(query="", fragment="")
    return urlunparse(stripped)

def get_base_domain(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    # Remove 'www.' if present
    if hostname.startswith('www.'):
        hostname = hostname[4:]
    return hostname
