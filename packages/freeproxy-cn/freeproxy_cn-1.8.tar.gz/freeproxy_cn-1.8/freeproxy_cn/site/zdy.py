from aiohttp.helpers import TOKEN, proxies_from_env
from freeproxy_cn.util.pipe import to_doc, head, to_dict
from freeproxy_cn.core.channel import Channel
from typing import List, Tuple
import base64
from logzero import logger
from dummy_useragent import UserAgent


class Zdy(Channel):
    site_name = 'www.zdaye.com'

    def __init__(self, **kwargs):
        super(Zdy, self).__init__(**kwargs)
        self.name = "zdaye"
        self.start_urls = ['https://www.zdaye.com/dayProxy.html']

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(
            self.session, url, headers={'User-Agent': UserAgent().random()})
        doc = content >> to_doc
        import pdb; pdb.set_trace()
        href = doc.xpath(
            '//div[@class="threadblock_list"]/div[@class="thread_item"]//a/@href'
        ) >> head
        href = f'https://www.zdaye.com{href}'
        content = await self.http_handler.get(
            self.session, url, headers={'User-Agent': UserAgent().random()})
        doc = content >> to_doc
        for item in doc.xpath('//div[@class="cont"]/text()'):
            if item.strip():
                host,port = item.strip().split('@')[0].split(":")
                proxies.append((host,port))
        return proxies
