import requests
from bs4 import BeautifulSoup
import pickle
import sys

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

login_data = {'name': 'Admin_Lauren', 'pass': 'Charlie#1', 'form_id': 'user_login', 'op': 'Log in', 'form_build_id': 'form-TdQbGTz8tJ3UgkQLM7nceXN_35dT6Cvq6CnuY76e3MU'}

userList = []

for pageNum in range(92):
    print( 'page = ', pageNum )
    with requests.Session() as a:
        user_url = 'https://www.boldnotionquilting.com/user/login?destination=admin/people%3Fpage%3D' + str(pageNum)
        r = a.post(user_url, data=login_data, headers=headers)
        soupA = BeautifulSoup(r.content,'html.parser')
        blocks = soupA.find_all("div", {"class": "form-type-checkbox"})
        for block in blocks:
            userNum = block.find('input')['value']
            userList.append( userNum )

with open('numbers', 'wb') as fp:
    pickle.dump(userList, fp)

