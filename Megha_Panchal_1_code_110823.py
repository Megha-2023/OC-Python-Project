"""Code to extract single book details from Books to Scrape website """
import requests
from bs4 import BeautifulSoup
import csv

#Column --> product_page_url
URL = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
web_page = requests.get(URL)

soup = BeautifulSoup(web_page.content,'html.parser')
#print(soup)
headers = ["product_page_url","book_title","upc","price_including_tax","price_excluding_tax","quantity_available","description","category","review_rating","image_url"]


#Column --> book_title 
book_title = soup.find_all("li",class_="active")[0].text
print(book_title)

product_table = soup.find("table",class_="table table-striped")
#for row in product_rows:
table_headers = soup.find_all("th")
header_values = soup.find_all("td")
dict = {}

#Columns --> upc,price_including_tax,price_excluding_tax,quantity_available
for i in range(len(table_headers)):
    index = table_headers[i].text.strip()
    value = header_values[i].text.strip()
    dict[index] = value
print(dict)

#Column --> description ## PENDING
description =""
#Column --> category ## PENDING
"""product_cat = soup.find_all("a")
for c in range(len(product_cat)):
    if "category" in (product_cat[c].text):
        category = product_cat[c].text
print(category)"""
category =""

#Column --> review_rating
rating =""
#Column --> image_url
image_url =""
images = soup.find_all("img")
for im in images:
    if im['alt'] == book_title:
        image_url = im['src']
        print(im['src'])


with open('data.csv','w',newline='') as file:
    writer = csv.writer(file,delimiter=',')
    writer.writerow(headers)

    data_row = [URL,book_title,dict['UPC'],dict['Price (incl. tax)'],dict['Price (excl. tax)'],dict['Availability'],description,category,rating,image_url]
    writer.writerow(data_row)

