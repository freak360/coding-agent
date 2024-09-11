import hmac
import hashlib

# Your webhook secret (from .env file)
# secret = 'c1f4171e7270316e84495432d77554ea95307290'

# The exact JSON payload as sent by Postman, including \r\n for newlines and carriage returns
payload = b'{\r\n  "ref": "refs/heads/main",\r\n  "before": "abc123",\r\n  "after": "def456",\r\n  "repository": {\r\n    "name": "coding-agent",\r\n    "url": "https://github.com/freak360/coding-agent"\r\n  },\r\n  "pusher": {\r\n    "name": "Aneeb Ajmal",\r\n    "email": "maneebajmal@gmail.com"\r\n  }\r\n}\r\n'

# Generate the HMAC SHA-256 signature
signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
print(f"sha256={signature}")
