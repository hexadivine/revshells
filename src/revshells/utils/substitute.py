import json
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "../assets"


def load_listener_context():
    with open(f'{ASSETS_DIR}/listeners_default_context.json') as listerners_context_file:
        return json.load(listerners_context_file)

def substitute(payload, ip, port, shell='', context={}):
    substituted_payload = payload.replace('{ip}', ip).replace('{port}', port).replace('{shell}', shell)

    DEFAULT_CONTEXT = load_listener_context()
    for key, item in context.items():
        DEFAULT_CONTEXT[key] = item
    
    for key, item in DEFAULT_CONTEXT.items():
        substituted_payload = substituted_payload.replace(f"{{{key}}}", item)
    
    return substituted_payload
