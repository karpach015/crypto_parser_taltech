import re
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup as Bs


class ErrorParser(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg


def get_coin_from_coin_market(url):
    html = requests.get(url).text
    soup = Bs(html, 'html.parser').select("tbody tr")
    data = set()
    try:
        for tr in soup:
            [data.add(coin['href']) for coin in tr.select("td")[2].select("a")]
    except Exception as e:
        raise ErrorParser(f"@Polo_Umen\n{e}\nfunc get_coin_from_coin_market\nLine: 14-15")

    return data


def get_coin_from_coin_gecko(url):
    html = requests.get(url)
    data = set()
    soup = Bs(html.content, 'html.parser').select("tbody tr td.coin-name a")
    [data.add(coin['href'][3:]) for coin in soup]
    return data


class MyParser:

    def __init__(self):
        self.urls_dict = {
            "site_map": "https://assets.coingecko.com/sitemap1.xml",
            "coin_market": "https://coinmarketcap.com/",
            "coin_gecko": "https://www.coingecko.com/en",
        }

    def parse_sitemap_coin_gecko(self):
        response = requests.get(self.urls_dict['site_map'])
        lines = [x for x in str(response.content).split("0.5") if "/coin" in x]

        all_coins = set()

        for line in lines:
            all_coins.add(re.findall(r'<loc>.+</loc>', line)[0][5:-6])

        return all_coins

    def parse_coin_market(self):
        all_urls = set()
        all_coins = set()
        try:
            response = requests.get(self.urls_dict['coin_market'])
            html = Bs(response.content, 'html.parser')
            page_num = int(html.select(".sc-8ccaqg-3 ul li")[-2].select("a")[0].text)
            all_urls = [f"{self.urls_dict['coin_market']}?page={page}" for page in range(1, page_num + 1)]
        except Exception as e:
            raise ErrorParser(f"@Polo_Umen\n{e}\nfunc parse_coin_market")

        with Pool(4) as p:
            coins = p.map(get_coin_from_coin_market, all_urls)

        [[all_coins.add(f"{self.urls_dict['coin_market'][:-1]}{coin}") for coin in coin_list] for coin_list in coins]
        return all_coins

    def parse_coin_market_new(self):
        all_coins = set()
        [all_coins.add(self.urls_dict['coin_market'][:-1] + coin) for coin in get_coin_from_coin_market(self.urls_dict['coin_market'] + "/new/")]
        return all_coins

    def parse_coin_gecko(self):
        all_coins = set()
        all_urls = []
        try:
            response = requests.get(self.urls_dict['coin_gecko'])
            html = Bs(response.content, 'html.parser')
            page_num = int(html.select("nav.pagy-bootstrap-nav ul li")[-2].select("a")[0].text)
            all_urls = [f"{self.urls_dict['coin_gecko']}?page={page}" for page in range(1, page_num + 1)]
        except Exception as e:
            raise ErrorParser(f"@Polo_Umen\n{e}\nfunc parse_coin_gecko")

        with Pool(8) as p:
            coins = p.map(get_coin_from_coin_gecko, all_urls)

        [[all_coins.add(f"{self.urls_dict['coin_gecko']}{coin}") for coin in coin_list] for coin_list in coins]

        return all_coins
