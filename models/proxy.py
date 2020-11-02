class Proxy:
    def __init__(self, proxy, proxy_type):
        self.proxy = proxy
        self.proxy_type = proxy_type

    def get_proxy(self):
        if None in [self.proxy, self.proxy_type]:
            return None

        return {
            'http':f'{self.proxy_type}://{self.proxy}',
            'https':f'{self.proxy_type}://{self.proxy}'
        }