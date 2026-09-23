# Security Rules & Anti-Patterns Reference

## 1. Connection Pool Exhaustion / Leaks

**CWE-400 / CWE-772**

### Vulnerable
```python
import aiohttp

async def fetch(url):
    session = aiohttp.ClientSession()   # never closed
    async with session.get(url) as resp:
        return await resp.text()
```

### Secure
```python
import aiohttp

async def fetch(url, session: aiohttp.ClientSession):
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        return await resp.text()

# Caller owns the session lifecycle
async with aiohttp.ClientSession() as session:
    data = await fetch("https://example.com", session)
```

## 2. Missing Timeouts on HTTP Clients

**CWE-400**

### Vulnerable
```python
import requests
resp = requests.get("https://api.example.com/data")  # can hang forever
```

### Secure
```python
import requests
resp = requests.get("https://api.example.com/data", timeout=(3.05, 10))
```

## 3. Race Conditions on Shared Mutable State (Async)

**CWE-362**

### Vulnerable
```python
counter = 0

async def increment():
    global counter
    tmp = counter
    await asyncio.sleep(0)          # yield point
    counter = tmp + 1
```

### Secure
```python
import asyncio
lock = asyncio.Lock()
counter = 0

async def increment():
    global counter
    async with lock:
        counter += 1
```

## 4. SQLite "database is locked"

**Common under concurrent writes**

### Vulnerable
```python
conn = sqlite3.connect("app.db")
# multiple threads/processes write without timeout or WAL
```

### Secure
```python
conn = sqlite3.connect("app.db", timeout=30.0)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=30000")
```

## 5. Hardcoded Secrets & High-Entropy Strings

**CWE-798 / CWE-312**

Detect patterns:
- AWS keys: `AKIA[0-9A-Z]{16}`
- Generic API keys / tokens with Shannon entropy > 4.5 and length ≥ 20
- Private keys: `-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----`

Never log the secret value. Report only location and fingerprint.

## 6. Unbounded Background Tasks

### Vulnerable
```python
asyncio.create_task(long_running_job())  # no reference, no cancellation
```

### Secure
```python
task = asyncio.create_task(long_running_job())
# store task and cancel on shutdown
```

## 7. SQL Injection

**CWE-89**

### Vulnerable
```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Secure
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

## 8. Insecure Deserialization

**CWE-502**

Avoid `pickle.loads` on untrusted data. Prefer JSON or explicit schema validation (pydantic / zod).

## Quick Checklist Before Production

- [ ] All HTTP clients have explicit timeouts
- [ ] Connection pools / sessions are closed or managed by context managers
- [ ] No hardcoded credentials in source
- [ ] Shared async state protected by locks or queues
- [ ] SQLite configured with WAL + busy_timeout if used concurrently
- [ ] Background tasks are tracked and cancellable
- [ ] Input validated before DB or shell use
