import requests
import io
import sys
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

#-------------------------

def getTitle(block):
    return block.find("div", {"class": "views-field-title"}).getText()

#-------------------------

def getPrice(block):
    x = block.find("div",{"class": "views-field-nothing"}).getText().split(", ")
    return x[0]

#-------------------------

def getAvailable(block):
    x = block.find("div",{"class": "views-field-nothing"}).getText().split(", ")
    return x[1]

#-------------------------

def getPicture(block):
    x = block.find("div",{"class": "views-field-field-product-image"}).img['src'].split('/')
    return x[-1] 

#-------------------------

def getLink(block):
    return 'https://boldnotionquilting.com'+(block.find("div",{"class": "views-field-field-product-image"}).a.get('href'))

#-------------------------

def getPage(link):
    page = urlopen(link)
    source = page.read()
    soup2 = BeautifulSoup(source,'html.parser')
    return soup2

#-------------------------

def getDescription(soup2):
    try:
        desc = soup2.find("meta", property="og:description").get("content")
    except: return 'N/A'
    return desc

#-------------------------

def getDimension(soup2):
    x = soup2.find("div",{"class": "field-type-physical-dimensions"}).getText().split(":")
    return x[1]

#-------------------------

def getWeight(soup2):
    x = soup2.find("div",{"class": "field-type-physical-weight"}).getText().split(":")
    return x[1]

#-------------------------

def getCategory(soup2):
    return soup2.find("div",{"class": "field-name-field-product-category"}).getText()
#-------------------------

#url = 'https://boldnotionquilting.com/products'

# Open text file with html source
html = open("html.txt", "r")

# Create beautifulsoup objects
soup = BeautifulSoup(html, 'html.parser')

# Get product block
blocks = soup.find_all("td", {"class": "product-view"})

d=[]
i=0
# Loop over blocks
for block in blocks:
    print( 'i=',i )
    title = getTitle(block)
    price = getPrice(block)
    available = getAvailable(block) 
    picture = getPicture(block) 
    link = getLink(block)
    soup2 = getPage(link)
    description = getDescription(soup2)
    dimension = getDimension(soup2)
    weight = getWeight(soup2)
    category = getCategory(soup2)
    d.append({'Title':title, 'Price':price, 'Available':available, 'Picture':picture, 'Description':description, 'Dimension':dimension, 'Weight':weight, 'Category':category})
    i  = i+1
    
df = pd.DataFrame(d)

print( df )
df.to_csv(r'quilting_data.csv')
