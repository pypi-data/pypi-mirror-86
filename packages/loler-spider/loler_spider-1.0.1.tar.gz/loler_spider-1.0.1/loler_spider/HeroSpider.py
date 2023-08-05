import requests
import json
from tqdm import tqdm
import os


class HeroSpider:
    def __init__(self):
        # 所有英雄ID的字典
        self.heros_id_dict = {}

        # 如果路径不存在则创建
        if not os.path.exists('./hero'):
            os.mkdir('hero')

        self._get_hero_id()

    def _get_hero_id(self):
        """获取所有英雄ID"""
        heros_id_url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
        res = requests.get(heros_id_url).content.decode('utf-8')
        json_data = json.loads(res)
        for hero in json_data['hero']:
            self.heros_id_dict.setdefault(hero['heroId'], f"{hero['name']}-{hero['title']}")

    def _json_parse(self, json_data):
        """解析英雄图片url"""
        json_data = json.loads(json_data)
        hero_img_url = None
        hero_name = None
        try:
            hero_img_url = json_data['skins'][0]['loadingImg']
            hero_name = json_data['skins'][0]['heroTitle']
        except:
            print("解析图片url失败!")
        return hero_img_url, hero_name

    # 下载英雄图片
    def _download_img(self, img_url, name):
        if img_url == None:
            return

        img_data = requests.get(img_url).content
        with open(f'./hero/{name}.jpg', 'wb') as f:
            f.write(img_data)

    def start(self):
        """获取英雄图片URL"""
        for page in tqdm(self.heros_id_dict):
            url = f"https://game.gtimg.cn/images/lol/act/img/js/hero/{page}.js"
            res = requests.get(url).content.decode('utf-8')
            hero_img_url, hero_name = self._json_parse(res)
            self._download_img(hero_img_url, hero_name)


h = HeroSpider()
h.start()
