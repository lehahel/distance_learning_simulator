def check_ip(ip):
    if not isinstance(ip, str):
        raise TypeError("ip should be string")
    ip_port = ip.split(':')
    if len(ip_port) != 2:
        return False
    if not ip_port[1].isdigit:
        return False
    if ip_port[0].replace(" ", "") == "localhost":
        return True
    first = ip_port[0].split('.')
    if len(first) != 4:
        return False
    for x in first:
        if not x.isdigit():
            return False
    return True
