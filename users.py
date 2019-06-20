import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
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

def getOrderNums(soup):
    orderList = []
    soup2 = soup.find("tbody")
    orders = soup2.find_all("td", {"class": "views-field-order-number"})
    for order in orders:
        orderList.append( order.find("a").getText() )
    return orderList

#------------------------

def getOrderInfo(soup):
    orderList = []
    soup2 = soup.find("tbody")
    blocks = soup2.find_all("tr")
    for block in blocks:
        placed = block.find("td", {"class": "views-field-placed"}).getText().strip()
        changed = block.find("td", {"class": "views-field-changed"}).getText().strip()
        subTotal = block.find("td", {"class": "views-field-commerce-order-total"}).getText().strip()
        status = block.find("td", {"class": "views-field-status"}).getText().strip()
        orderList.append( (placed, changed, subTotal, status) )
    return orderList

#------------------------

def getOrderSpecifics(soup):
    
    

#------------------------

def getItemSpecifics(soup):
    

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

    print( 'userNum: ', userNum )

    #Open user page and get info
    with requests.Session() as a:
        user_url = 'https://boldnotionquilting.com/user/login?destination=user/' + userNum
        r = a.post(user_url, data=login_data, headers=headers)
        soupA = BeautifulSoup(r.content,'html.parser')
        username = getUsername(soupA)
        email = getEmail(soupA)
        dateJoined = getJoined(soupA)
        first = getFirst(soupA)
        last = getLast(soupA)
        home = getHome(soupA)
        fb = getFb(soupA)

    orderNums = []
    # Open orders page
    with requests.Session() as b:
        order_url = 'https://boldnotionquilting.com/user/login?destination=user/' + userNum + '/orders'
        r = b.post(order_url, data=login_data, headers=headers)
        soupB = BeautifulSoup(r.content,'html.parser')

        # If there are no orders, then skip
        if soupB.find("tbody").find("a").getText() == 'APQS Machine Inquiries or Service': continue

        # Get order info (orderNum, placed, updated, subTotal, status)
        orderNums = getOrderNums(soupB)
        orderInfo = getOrderInfo(soupB)

    orderArray = []
    # Loop over order numbers
    for order in orderNums:
        
        # Open order page
        with requests.Session() as c:
            spec_url = 'https://boldnotionquilting.com/user/login?destination=user/' + userNum + '/orders/' + orderNum
            r = c.post(spec_url, data=login_data, headers=headers)
            soupC = BeautifulSoup(r.content,'html.parser')
            
            # Get order specifics (items, unit price, quantity, total, shipping, billingInfo, shippingInfo)
            print( getItemSpecifics(soupC) )
            print( getOrderSpecifics(soupC) )

        # Build complete order list/array by appending elements

    # Append user to csv
    # Export user orders to its own csv file 
