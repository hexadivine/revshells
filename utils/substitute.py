def substitute(payload, ip, port, shell=''):
        return payload.replace('{ip}', ip).replace('{port}', port).replace('{shell}', shell)
