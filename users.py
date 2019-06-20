import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import csv
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
    try: 
        ship = soup.find("tr", {"class": "component-type-shipping"}).find("td", {"class": "component-total"}).getText()
    except: 
        try: ship = soup.find("tr", {"class": "component-type-flat-rate-basic-flat-rate-shipping"}).find("td", {"class": "component-total"}).getText()
        except: ship = '$0.00'
    try:
        tax = soup.find("tr", {"class": "component-type-taxfl-tax-rate"}).find("td", {"class": "component-total"}).getText()
    except: tax = '$0.00'
    shipInfo = getAddress(soup,'shipping')
    billInfo = getAddress(soup,'billing')
    specList = (ship, tax, shipInfo, billInfo) 
    return specList
    
#------------------------

def getAddress(soup,type):
    address = []
    soup2 = soup.find("div", {"class": "field-name-commerce-customer-" + type})
    street = soup2.find("div", {"class": "street-block"}).getText()
    city = soup2.find("span", {"class":"locality"}).getText()
    state = soup2.find("span", {"class":"state"}).getText()
    zip= soup2.find("span", {"class":"postal-code"}).getText()
    address = street + ', ' + city + ', ' + state + ', ' + zip
    return address

#------------------------

def getItemSpecifics(soup):
    itemList = []
    soup2 = soup.find("tbody")
    blocks = soup2.find_all("tr")
    for block in blocks:
        title = block.find("td", {"class": "views-field-line-item-title"}).getText().strip()
        price = block.find("td", {"class": "views-field-commerce-unit-price"}).getText().strip()
        quantity = block.find("td", {"class": "views-field-quantity"}).getText().strip()
        total = block.find("td", {"class": "views-field-commerce-total"}).getText().strip()
        itemList.append( (title, price, quantity, total) )
    return itemList

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

    userArray = {'userNum': userNum, 'Username': username, 'email': email, 'dateJoined': dateJoined, 'First Name': first, 'Last Name': last, 'Hometown': home, 'Facebook': fb}
    #userArray = ( userNum, username, email, dateJoined, first, last, home, fb )

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
    iter = 0
    # Loop over order numbers
    for order in orderNums:

        # Open order page
        with requests.Session() as c:
            spec_url = 'https://boldnotionquilting.com/user/login?destination=user/' + userNum + '/orders/' + order
            r = c.post(spec_url, data=login_data, headers=headers)
            soupC = BeautifulSoup(r.content,'html.parser')
            
            # Get order specifics (items, unit price, quantity, total, shipping, billingInfo, shippingInfo)
            itemSpec = getItemSpecifics(soupC)
            orderSpec = getOrderSpecifics(soupC)
            
        # Build complete order list/array by appending elements
        # order 
        # orderInfo: placed, changed, subTotal, status
        # itemSpec: loop (title, price, quantity, total)
        # orderSpec: ship, tax, shipInfo, billInfo
        orderArray.append( {'Order Number': order, \
                                'Order Placed': orderInfo[iter][0], \
                                'Order Changed': orderInfo[iter][1], \
                                'Order Status': orderInfo[iter][3], \
                                'Order Shipping': orderSpec[0], \
                                'Order Total': orderInfo[iter][2], \
                                'Order Products': [i[0] for i in itemSpec], \
                                'Unit Price': [i[1] for i in itemSpec],\
                                'Quantity': [i[2] for i in itemSpec],\
                                'Total': [i[3] for i in itemSpec], \
                                'Tax': orderSpec[1], \
                                'Shipping Address': orderSpec[2],\
                                'Billing Address': orderSpec[3]
                            } )

        iter += 1

    df = pd.DataFrame( orderArray )

    # Append user to csv
    fieldnames = ['userNum', 'Username', 'email', 'dateJoined', 'First Name', 'Last Name', 'Hometown', 'Facebook']
    with open('userInformation.csv','a', newline='') as fd:
        writer = csv.DictWriter(fd,fieldnames=fieldnames)
        writer.writerow(userArray)

    # Export user orders to its own csv file 
    df.to_csv('orders/' + userNum + '_orders.csv')

