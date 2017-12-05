import requests
from bs4 import BeautifulSoup as bs

headers = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,da;q=0.5',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'authority': 'search.naver.com',
}

params = (
    ('query', '넥슨'),
)

res = requests.get(
    'https://search.naver.com/search.naver', 
    headers=headers, 
    params=params
)
html = res.text

soup = bs(html, 'lxml')

link_list = soup.select('.news.section a')

for link in link_list:
    print(link.text)
