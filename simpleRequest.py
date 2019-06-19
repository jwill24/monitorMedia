import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

login_data = {
    'name': 'Admin_Lauren',
    'pass': 'Charlie#1',
    'form_id': 'user_login',
    'op': 'Log in'
}

with requests.Session() as s:
    url = 'https://boldnotionquilting.com/user/login'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['form_build_id'] = soup.find('input', attrs={'name': 'form_build_id'})['value']
    
    people_url = 'https://boldnotionquilting.com/user/login?destination=admin/people'
    r = s.post(people_url, data=login_data, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')

print(soup)
