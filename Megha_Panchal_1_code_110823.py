"""Code to extract single book details from Books to Scrape website """
import requests
from bs4 import BeautifulSoup
import csv

#Column --> product_page_url
URL = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
Category_URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

def get_product_details(product_url):

    web_page = requests.get(product_url)

    soup = BeautifulSoup(web_page.content,'html.parser')
    #print(soup)
    headers = ["product_page_url","book_title","upc","price_including_tax","price_excluding_tax","quantity_available","description","category","review_rating","image_url"]


    #Column --> book_title 
    book_title = soup.find_all("li",class_="active")[0].text

    #retrive table details
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
    description =soup.find("article",class_="product_page").select("p")[3].get_text(strip=True)
    #print(description)

    #Column --> category ## PENDING
    category = soup.find("ul",class_="breadcrumb").select("li")[1].find("a").get_text(strip=True)
    print(category)

    #Column --> review_rating
    rating = soup.find("article",class_="product_page").select("p")[2]
    review_rating = rating['class'][1]
    print(review_rating)

    #Column --> image_url
    image_url =""
    images = soup.find_all("img")
    for im in images:
        if im['alt'] == book_title:
            image_url = im['src']
    image_url = image_url.replace("../..","http://books.toscrape.com/")
    print(image_url)

    
    with open('data.csv','w',newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(headers)

        data_row = [product_url,book_title,dict['UPC'],dict['Price (incl. tax)'],dict['Price (excl. tax)'],dict['Availability'],description,category,review_rating,image_url]
        writer.writerow(data_row)
    


get_product_details(URL)