# Security Checklist (OWASP Top 10 Condensed)

Use this checklist when reviewing code changes. For each category, grep for the listed patterns and inspect matches in the diff.

---

## 1. Injection (SQL, NoSQL, Command, Template)

**Grep patterns:**
```
query(           — raw SQL queries
exec(            — command execution
eval(            — code evaluation
system(          — system calls
subprocess       — Python subprocess
child_process    — Node.js child process
${               — template literals in queries
f"               — Python f-strings in queries
.format(         — Python format strings in queries
% (              — Python % formatting in queries
```

**What to check:**
- Are user inputs parameterized/escaped before use in queries?
- Are shell commands built from user input?
- Is `eval()` or equivalent used with dynamic input?

---

## 2. Broken Authentication

**Grep patterns:**
```
password         — hardcoded passwords
secret           — hardcoded secrets
token            — token handling
jwt              — JWT implementation
session          — session management
cookie           — cookie settings
httpOnly         — cookie security flags
secure:          — secure flag on cookies
sameSite         — CSRF protection
bcrypt           — password hashing
argon2           — password hashing
md5              — weak hashing (red flag)
sha1             — weak hashing (red flag)
```

**What to check:**
- Are passwords hashed with bcrypt/argon2 (not MD5/SHA1)?
- Do JWTs have expiration and proper validation?
- Are session cookies httpOnly, secure, sameSite?
- Is there rate limiting on auth endpoints?

---

## 3. Sensitive Data Exposure

**Grep patterns:**
```
console.log      — logging sensitive data
print(           — logging sensitive data
logger.          — logging sensitive data
.env             — environment file references
process.env      — environment variable access
os.environ       — Python environment access
API_KEY          — API key references
SECRET           — secret references
PASSWORD         — password references
PRIVATE_KEY      — private key references
credential       — credential references
```

**What to check:**
- Are secrets loaded from environment variables (not hardcoded)?
- Is sensitive data excluded from logs?
- Are API keys, tokens, passwords in `.gitignore`?
- Is PII encrypted at rest and in transit?

---

## 4. XML External Entities (XXE)

**Grep patterns:**
```
xml.parse        — XML parsing
DOMParser        — browser XML parsing
lxml             — Python XML
etree            — Python XML
<!ENTITY         — XML entity declarations
```

**What to check:**
- Is external entity processing disabled?
- Are XML parsers configured securely?

---

## 5. Broken Access Control

**Grep patterns:**
```
isAdmin          — admin checks
role             — role-based access
permission       — permission checks
authorize        — authorization logic
@auth            — auth decorators
middleware       — middleware (auth)
req.user         — user from request
currentUser      — current user reference
req.params.id    — user-controlled IDs (IDOR risk)
```

**What to check:**
- Does every endpoint check authorization (not just authentication)?
- Are object IDs validated against the current user (prevent IDOR)?
- Is there server-side access control (not just UI hiding)?
- Are admin routes protected?

---

## 6. Security Misconfiguration

**Grep patterns:**
```
CORS             — CORS configuration
Access-Control   — CORS headers
origin: '*'      — permissive CORS (red flag)
debug            — debug mode
DEBUG = True     — Python debug mode
NODE_ENV         — environment setting
helmet           — security headers (Node.js)
X-Frame-Options  — clickjacking protection
Content-Security — CSP headers
```

**What to check:**
- Is CORS configured to specific origins (not `*`)?
- Is debug mode off in production?
- Are security headers set (CSP, X-Frame-Options, HSTS)?
- Are default credentials changed?

---

## 7. Cross-Site Scripting (XSS)

**Grep patterns:**
```
innerHTML        — direct HTML insertion
dangerouslySetInnerHTML  — React raw HTML
v-html           — Vue raw HTML
{!! !!}          — Laravel unescaped output
| safe            — Django/Jinja safe filter
document.write   — DOM manipulation
.html(           — jQuery HTML insertion
DOMPurify        — sanitization library (good sign)
sanitize         — sanitization
escape           — escaping
```

**What to check:**
- Is all user-generated content escaped before rendering?
- Is `dangerouslySetInnerHTML` / `innerHTML` used with sanitized content?
- Are URL parameters reflected without encoding?

---

## 8. Insecure Deserialization

**Grep patterns:**
```
JSON.parse       — JSON deserialization
pickle           — Python pickle (dangerous)
yaml.load        — YAML loading (use safe_load)
unserialize      — PHP deserialization
Marshal.load     — Ruby deserialization
deserialize      — generic deserialization
```

**What to check:**
- Is `pickle` used with untrusted data? (Critical vulnerability)
- Is `yaml.load` used instead of `yaml.safe_load`?
- Is deserialized data validated before use?

---

## 9. Using Components with Known Vulnerabilities

**Check commands:**
```bash
npm audit                          # Node.js
pip-audit                          # Python
bundle audit                       # Ruby
composer audit                     # PHP
govulncheck ./...                  # Go
cargo audit                        # Rust
```

**What to check:**
- Are dependencies up to date?
- Are there known vulnerabilities in direct dependencies?
- Is there a lockfile committed?

---

## 10. Insufficient Logging & Monitoring

**Grep patterns:**
```
catch            — error handling (are errors logged?)
except           — Python error handling
rescue           — Ruby error handling
console.error    — client-side error logging
logger.error     — server-side error logging
winston          — logging library
pino             — logging library
```

**What to check:**
- Are authentication failures logged?
- Are authorization failures logged?
- Are errors caught and logged (not swallowed)?
- Do logs include enough context for debugging without sensitive data?
