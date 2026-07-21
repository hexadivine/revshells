import subprocess

def get_interfaces():
    cmd = "ip a | grep -E '^[0-9]+:' | cut -d' ' -f2 | tr '\n' ','"
    interfaces = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
    interfaces_list = interfaces.split(':,')[:-1]
    return interfaces_list