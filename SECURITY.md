# Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, report them by opening a [private security advisory](https://github.com/kennethsolomon/shipkit/security/advisories/new) on GitHub, or email **hello@kennethsolomon.com** directly.

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix timeline**: Depends on severity:
  - Critical: 24–48 hours
  - High: 1 week
  - Medium/Low: Next release

## Scope

Security issues in the ShipKit codebase that could:
- Execute arbitrary code on user machines
- Expose sensitive data (API keys, credentials, env files)
- Compromise the integrity of generated plans or code
- Allow prompt injection through malicious project files

## Protecting Your Projects

ShipKit instructs Claude to read and write files in your project. Add a deny list to `.claude/settings.json` to prevent Claude from accessing sensitive files:

```json
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Read(**/*.p12)",
      "Read(**/credentials*)"
    ]
  }
}
```

## Recognition

We appreciate responsible disclosure and will credit reporters in release notes unless you prefer to remain anonymous.
