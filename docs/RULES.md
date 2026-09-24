# Rules & Finding Model

## Unified finding shape

```json
{
  "rule_id": "missing-http-timeout",
  "category": "reliability",
  "severity": "MEDIUM",
  "confidence": 0.94,
  "file": "src/api.py",
  "line": 42,
  "message": "HTTP request does not specify a timeout",
  "remediation": "Add an explicit timeout",
  "cwe": "CWE-400"
}
```

Severity and confidence are independent.

## Policy

- `PASS` — no critical/high (configurable)
- `WARN` — medium/low only
- `FAIL` — critical or high present (default gate)

Configured via `skills/production-hardening/schemas/audit_config.json` → `fail_on_severity`.
