import re
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup as Bs


def make_all(url):
    html = requests.get(url).text
    data = set()
    soup = Bs(html, 'html.parser').select("tbody tr")
    for tr in soup:
        [data.add(coin['href']) for coin in tr.select("td")[2].select("a")]

    return data


class MyParser:

    def __init__(self):
        self.urls_dict = {
            "site_map": "https://assets.coingecko.com/sitemap1.xml",
            "coin_market": "https://coinmarketcap.com/",
            "coin_gecko": "https://www.coingecko.com/en"
        }

    def parse_sitemap_coin_gecko(self):
        response = requests.get(self.urls_dict['site_map'])
        lines = [x for x in str(response.content).split("0.5") if "/coin" in x]

        all_coins = set()

        for line in lines:
            all_coins.add(re.findall(r'<loc>.+</loc>', line)[0][5:-6])

        return all_coins

    def parse_coin_market(self):
        response = requests.get(self.urls_dict['coin_market'])
        html = Bs(response.content, 'html.parser')
        page_num = int(html.select(".sc-8ccaqg-3 ul li")[-2].select("a")[0].text)
        all_coins = set()
        all_urls = [f"{self.urls_dict['coin_market']}?page={page}" for page in range(1, page_num + 1)]

        with Pool(8) as p:
            coins = p.map(make_all, all_urls)

        [[all_coins.add(f"{self.urls_dict['coin_market'][:-1]}{coin}") for coin in coin_list] for coin_list in coins]
        return all_coins

    def parse_coin_gecko(self):
        response = requests.get(self.urls_dict['coin_gecko'])
        html = Bs(response.content, 'html.parser')
        page_num = int(html.select("nav.pagy-bootstrap-nav ul li")[-2].select("a")[0].text)
        all_coins = set()

        for i in range(1, page_num + 1):
            page_response = requests.get(f"{self.urls_dict['coin_gecko']}?page={i}")
            [all_coins.add(coin['href']) for coin in
             Bs(page_response.content, 'html.parser').select("tbody tr td.coin-name a")]

        return all_coins
