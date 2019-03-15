import requests

def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过20秒的代理就不要了
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            # logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        # logger.error(str(e))
        return False