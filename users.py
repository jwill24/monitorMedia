import requests
from bs4 import BeautifulSoup


#------------------------

def getUsername:
    


#------------------------

# List
# url for page 1: https://www.boldnotionquilting.com/user/login?destination=admin/people%3Fpage%3D0
# url for page 2: https://www.boldnotionquilting.com/user/login?destination=admin/people%3Fpage%3D1
# url for page 3: https://www.boldnotionquilting.com/user/login?destination=admin/people%3Fpage%3D2

# Individual
# url for hunterparadis33: https://www.boldnotionquilting.com/user/login?destination=user/4739
# list page uses: 4738

# Fields needed
# Main page: username, status, memberFor, lastAccess, 
# Individual page: First name, last name, hometown, facebook, email, dateJoined, badgesEarned, courseResults

 
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
