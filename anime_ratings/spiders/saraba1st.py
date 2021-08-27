import datetime as dt
import re

import scrapy
from anime_ratings.items import AnimeRatingsItem
from tqdm import tqdm


class Saraba1stSpider(scrapy.Spider):
    name = 'saraba1st'
    allowed_domains = ['bbs.saraba1st.com']
    max_page = 45
    start_urls = [
        f'http://bbs.saraba1st.com/2b/forum-83-{i}.html' for i in range(1, max_page+1)]

    def start_requests(self):
        self.pbar = tqdm(total=len(self.start_urls))
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse, dont_filter=True)

    custom_settings = {
        'LOG_LEVEL': 'WARNING'
    }
    handle_httpstatus_list = [404]

    def parse(self, response):
        match = re.search(
            '^https://bbs\.saraba1st\.com/2b/forum-83-(.*).html$', response.url)
        page = int(match.group(1))

        results = []
        subjects = response.css('.s::text').getall()

        for subject in subjects:
            match = re.search('^(\[TV\] )?\[(.*)\]\[(.*?)\](.*)$', subject)
            if match is None:
                continue
            date = match.group(2)
            year, month = date.split('.') if len(
                date.split('.')) == 2 else date.split('/')
            date = f'{year}-{int(month):02d}'

            info = match.group(3)
            m = re.search(r"^(TV|MOV|OVA|WEB)+\.?(.*)$", info, re.IGNORECASE)
            type = m.group(1)
            episode = m.group(2) or 1
            title = match.group(4).strip()
            if not title.startswith('Fate'):
                title = title.split('/')[0].strip().replace('&#39;', "'")
            else:
                title = title.split('/Fate')[0].strip()
            result = f'{date},"{title}",{type},{episode}'
            results.append(result)

        yield AnimeRatingsItem(page=page, results=results)
