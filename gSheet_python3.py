#!/usr/bin/python
import requests
import io
import sys


url = 'https://docs.google.com/spreadsheets/d/1hiFpMDWEKYIAMJdnp45Vm8thqdTIET4GwlCnZypSfWw/export?format=csv&gid=0'
html = requests.get(url).content.decode('utf-8')
rows = html.splitlines()


for row in rows:
    if str( sys.argv[1] ) in row:
        print( row )



