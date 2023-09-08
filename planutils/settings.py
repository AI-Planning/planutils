
import json, os

from planutils import manifest_converter

# This should eventually be changed once the prefix is customizable
PLANUTILS_PREFIX = os.path.join(os.path.expanduser('~'), '.planutils')

SETTINGS_FILE = os.path.join(PLANUTILS_PREFIX, 'settings.json')

DEFAULT_PAAS_SERVER = 'https://paas-uom.org:5001'
DEFAULT_PAAS_SERVER_LIMIT = 100

def load():
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.loads(f.read())
    return settings

def save(s):
    if 'PAAS_SERVER' not in s:
        s['PAAS_SERVER'] = DEFAULT_PAAS_SERVER
    if 'PAAS_SERVER_LIMIT' not in s:
        s['PAAS_SERVER_LIMIT'] = DEFAULT_PAAS_SERVER_LIMIT
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(s))
    manifest_converter.generate_manifest()
