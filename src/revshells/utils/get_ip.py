from revshells.utils.get_interfaces import get_interfaces
import subprocess

def get_ip(interface):
    valid_interfaces = get_interfaces()
    if (interface not in valid_interfaces):
        return ''
    
    cmd = f"ip -4 addr show {interface} | grep 'inet' | cut -d' ' -f 6 | cut -d'/' -f 1"
    ip = subprocess.run(cmd, capture_output=True, shell=True, text=True).stdout.rstrip().lstrip()
    ip = '127.0.0.1' if ip == '' else ip
    return ip