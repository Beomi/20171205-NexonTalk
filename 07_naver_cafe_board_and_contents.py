from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import json
import time
import random

keys = json.load(open('naver.json'))

# naver.json파일
# {
#     "id": "아이디",
#     "pw": "패스워드"
# }

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

def get_cookies(user_id, user_pw):
    driver = webdriver.Chrome('chromedriver')
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_css_selector('#id').send_keys(user_id)
    driver.find_element_by_css_selector('#pw').send_keys(user_pw)
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
    cookie = driver.get_cookies()
    driver.quit()
    return cookie

with requests.Session() as s:
    s.headers = {
        'accept-language': 'ko-KR,ko',
        'user-agent': USER_AGENT,
        'accept': '*/*',
    }
    cookie_jar = get_cookies(keys['id'], keys['pw'])
    for cookie in cookie_jar:
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    
    # 1페이지부터 5페이지 내 게시글 URL 가져오기
    url_list = []
    for pageno in range(1, 6):
        print('Page: ', pageno)
        res = s.get(
            'http://cafe.naver.com/ArticleList.nhn?search.clubid={clubid}&search.menuid={menuid}&search.boardtype=L&search.page={pageno}'.format(
                clubid='28385054',
                menuid='53',
                pageno=pageno
            )
        )
        soup = bs(res.text, 'lxml')
        article_link_list = soup.select('td.board-list span > a')
        for article in article_link_list:
            article_url = article['href']
            url_list.append(article_url)
        print('URL counter: ', len(url_list))

    # 중복 URL 거르기
    url_list = set(url_list)
    print('전체 URL개수: ', len(url_list))

    # 앞서 가져온 URL 내용 가져오기 (제목, 본문)
    contents_list = []
    for url in url_list:
        url = 'http://cafe.naver.com' + url
        res2 = s.get(url)
        soup = bs(res2.text, 'lxml')
        title = soup.select_one('div.tit-box span.b.m-tcol-c')
        content = soup.select_one('#tbody')
        url = soup.select_one('#linkUrl')
        date = soup.select_one('td.date')
        content_dic = {
            'title': title.text,
            'content': ' '.join(content.text.split()),
            'url': url.text,
            'date': date.text
        }
        contents_list.append(content_dic)
        print(content_dic)
        sleep_time = random.random() * 2
        print('Wait for.. ', sleep_time, 'seconds.')
        time.sleep(sleep_time)
    json.dump(contents_list, open('maplem_cafe.json', 'w+'))
