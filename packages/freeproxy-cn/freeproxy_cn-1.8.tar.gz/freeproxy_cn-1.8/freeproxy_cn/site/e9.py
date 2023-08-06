from freeproxy_cn.core.channel import Channel


class E9(Channel):
    site_name = 'www.89ip.cn'

    def __init__(self, **kwargs):
        super(E9, self).__init__(**kwargs)
        self.url_plt = 'https://www.89ip.cn/index_%s.html'

    async def bootstrap(self):
        urls = []
        for i in range(10):
            urls.append(self.url_plt % i)
        self.start_urls = urls
