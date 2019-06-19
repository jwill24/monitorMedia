import requests
from bs4 import BeautifulSoup
import pickle
import sys

#------------------------

def getUsername(soup):
    return soup.find("div", {"class": "profile-name"}).getText()

#------------------------

def getEmail(soup):
    return soup.find("div", {"class": "profile-email"}).getText()

#------------------------

def getJoined(soup):
    return soup.find("div", {"class": "d-inline-block mx-3"}).find("span").getText()

#------------------------

def getFirst(soup):
    return soup.find("div", {"class": "field-name-field-first-name"}).find("div", {"class": "field-item even"}).getText()

#------------------------

def getLast(soup):
    return soup.find("div", {"class": "field-name-field-last-name"}).find("div", {"class": "field-item even"}).getText()

#------------------------

def getHome(soup):
    try:
        hometown = soup.find("div", {"class": "field-name-field-hometown"}).find("div", {"class": "field-item even"}).getText()
    except: return 'N/A'
    return hometown

#------------------------

def getFb(soup):
    try:
        fb = soup.find("div", {"class": "field-name-field-facebook-profile"}).find("div", {"class": "field-item even"}).getText()
    except: return 'N/A'
    return fb
#------------------------

#------------------------

#------------------------

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

login_data = {'name': 'Admin_Lauren', 'pass': 'Charlie#1', 'form_id': 'user_login', 'op': 'Log in', 'form_build_id': 'form-TdQbGTz8tJ3UgkQLM7nceXN_35dT6Cvq6CnuY76e3MU'}

# Get list of valid userNums from file
with open ('numbers', 'rb') as fp:
    validEntries = pickle.load(fp)

# Loop over users
for userNum in validEntries:

    #Open user page and get info
    with requests.Session() as a:
        user_url = 'https://boldnotionquilting.com/user/login?destination=user/' + str(userNum)
        r = a.post(user_url, data=login_data, headers=headers)
        soupA = BeautifulSoup(r.content,'html.parser')
        username = getUsername(soupA)
        email = getEmail(soupA)
        dateJoined = getJoined(soupA)
        first = getFirst(soupA)
        last = getLast(soupA)
        home = getHome(soupA)
        fb = getFb(soupA)

    # Open orders page
    with requests.Session() as b:
        order_url = 'https://boldnotionquilting.com/user/login?destination=user/' + userNum + '/orders'
        r = b.post(user_url, data=login_data, headers=headers)
        soupB = BeautifulSoup(r.content,'html.parser')

        # Get order info (orderNum, placed, updated, total, status)
        # Pull table as pandas df
        

    # Open specific order page
