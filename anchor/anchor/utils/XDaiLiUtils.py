import time

import hashlib


def get_sign(orderno, secret, timestamp):

    string = "orderno={orderno},secret={secret},timestamp={timestamp}".format(
        orderno=orderno, secret=secret, timestamp=timestamp
    )

    return hashlib.md5(string.encode("utf-8")).hexdigest().upper()


def get_proxy_header(ip_port, secret_orderno):

    ip, port = ip_port

    ip_port = ip + ":" + port

    secret, orderno = secret_orderno

    timestamp = str(int(time.time()))

    sign = get_sign(orderno=orderno, secret=secret, timestamp=timestamp)

    auth = "sign={sign}&orderno={orderno}&timestamp={timestamp}".format(
        sign=sign, orderno=orderno, timestamp=timestamp
    )

    return "http://" + ip_port, auth


