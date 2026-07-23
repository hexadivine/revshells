from urllib.parse import quote
import base64 as b64

def base64(payload):
    return b64.b64encode(payload.encode()).decode()

def base32(payload):
    return b64.b32encode(payload.encode()).decode()

def safe_url_encode(payload):
    return quote(payload, safe="")

def url_encode(payload):
    return quote(payload)

def double_url_encode(payload):
    return quote(quote(payload))

def double_safe_url_encode(payload):
    return quote(quote(payload, safe=""), safe="")
