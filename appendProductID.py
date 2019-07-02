import sys
import csv
import os
import re
import pandas as pd
import pickle

#---------------------------

def getPercent(price):
    return price*0.2

#---------------------------

def getMatches(productInfo,productID):
    # Loop over product info list                                                                                                                                           
    for vec in productInfo:
        
        productPrice = re.split( char_regex,vec['Price'].strip() )
        orderPrice = re.split( char_regex,price.strip() )

        titleMatch = vec['Title'].strip() == product.strip()
        percent = getPercent( int(productPrice[1]) )
        try: priceGreater = int(productPrice[1]) - percent <= int(orderPrice[1])
        except: priceGreater = False
        try: priceLess = int(productPrice[1]) + percent >= int(orderPrice[1])
        except: priceLess = False
        priceMatch = priceGreater and priceLess

        if titleMatch and priceMatch:
            productID = vec['ID'].strip()

    return productID

#---------------------------

regex = '\(([^)]+)\)[^)]*\Z' # Remove last parentheses
char_regex = r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]' # Split special characters

# Get list of product IDs
with open ('IDs', 'rb') as fp:
    productInfo = pickle.load(fp)

# Loop over all order files
for filename in os.listdir('orders'):

    lines = []

    with open('orders/'+filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Loop over product in file
        for row in csv_reader:
            if row[11] == 'Order Products':
                row.insert(11,'Product ID')
                lines.append(row)
            else:
                # Get product name and price
                product = re.sub(regex, '', row[11])
                price = row[12]
                productID = 'N/A'

                # If og product, get id from title
                if 'product-og' in row[11]:
                    productID = re.search(r'\d+',row[11]).group()

                # Get the product id based on the title
                productID = getMatches(productInfo,productID)

                # Append product ID in list
                row.insert(11,productID)
                lines.append(row)

    # Write the updated lines to file
    with open('orders/'+filename,'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows( lines )
        
