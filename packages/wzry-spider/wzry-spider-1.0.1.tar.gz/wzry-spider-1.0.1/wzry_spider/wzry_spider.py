import os

from lxml import etree
import requests
from tqdm import tqdm


class wzry(object):
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36"
        }

    def hero(self):
        response = requests.get("https://pvp.qq.com/web201605/herolist.shtml", headers=self.headers).text
        html = etree.HTML(response)
        hero_list = html.xpath('//ul[@class="herolist clearfix"]/li/a/@href')
        for url in tqdm(hero_list):
            full_url = "https://pvp.qq.com/web201605/" + url
            response = requests.get(full_url, headers=self.headers).content.decode('gbk')
            html = etree.HTML(response)
            p_name_list = html.xpath('//ul[@class="pic-pf-list pic-pf-list3"]/@data-imgname')[0].split('|')
            p_src = html.xpath('//div[@class="zk-con1 zk-con"]/@style')[0].split('(')[1].split(')')[0].strip(
                "'//1.jpg'")
            num = len(p_name_list)
            hero_name = html.xpath('//h2[@class="cover-name"]/text()')[0]
            os.makedirs(f'king/{hero_name}')
            for i in range(0, num):
                p_url = "https://" + "g" + p_src + f'{i + 1}.jpg'
                response = requests.get(p_url, headers=self.headers).content
                with open(f'king/{hero_name}/{p_name_list[i].split("&")[0]}.jpg', 'wb') as f:
                    f.write(response)
