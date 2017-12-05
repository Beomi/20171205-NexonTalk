from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import json

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
        print(cookie)
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    res = s.get('https://nid.naver.com/user2/help/myInfo.nhn?lang=ko_KR')
    soup = bs(res.text, 'html.parser')
    nickname = soup.select_one('dd.nic_desc')
    print('내 닉네임은: ',nickname.text)
