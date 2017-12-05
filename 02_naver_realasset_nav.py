# 네이버 부동산 '글자' 가져오기
import requests
from bs4 import BeautifulSoup as bs


req = requests.get('http://naver.com')
html = req.text

soup = bs(html, 'lxml')

부동산 = soup.select_one(
    '#PM_ID_serviceNavi > li:nth-of-type(4) > a > span.an_txt'
)

print(부동산.text)

