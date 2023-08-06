from freeproxy_cn.util.pipe import to_dict, to_doc, head
from freeproxy_cn.core.channel import Channel
from typing import List, Tuple


class NiMa(Channel):
    site_name = 'nimadaili.com'

    def __init__(self, **kwargs):
        super(NiMa, self).__init__(**kwargs)
        self.name = "nimadaili"
        self.url_plt = [
            "http://www.nimadaili.com/https/%d/",
            "http://www.nimadaili.com/http/%d/"
        ]

    async def bootstrap(self):
        urls = []
        for i in range(1, 3):
            urls += [plt % i for plt in self.url_plt]
        self.start_urls = urls

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        proxies = []
        for item in doc.xpath('//tbody/tr'):
            proxy = item.xpath('./td/text()') >> head
            host, port = proxy.strip().split(':')
            proxies.append((host, port))
        return proxies