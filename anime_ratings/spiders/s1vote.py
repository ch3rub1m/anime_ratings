import os

import scrapy


class S1voteSpider(scrapy.Spider):
    name = 's1vote'
    allowed_domains = ['s1vote.com']
    start_urls = ['http://s1vote.com/']

    custom_settings = {
        'LOG_LEVEL': 'ERROR'
    }

    def parse(self, response):
        s = 'title,score,votes_count,dispute\n'
        rows = response.css('.main_table tr')
        for row in rows:
            attributes = row.css('td::text').getall()
            if len(attributes) == 0:
                continue
            title = row.css('td a::text').get().strip()
            title = title[title.startswith('[TV.13]') and len('[TV.13]'):]
            score = attributes[1]
            votes_count = attributes[2]
            dispute = attributes[5]
            s += f'"{title}",{score},{votes_count},{dispute}\n'

        filename = f'{self.name}.csv'
        home = os.path.expanduser('~')
        path = getattr(self, 'path', f'{home}/Documents')
        filepath = f'{path}/{filename}'
        with open(filepath, 'w') as f:
            f.write(s)
