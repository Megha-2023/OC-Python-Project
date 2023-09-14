"""Code to extract single book details from Books to Scrape website """
import requests
from bs4 import BeautifulSoup
import csv

#Column --> product_page_url
URL = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
Category_URL = "http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html"

def get_product_details(product_url):

    web_page = requests.get(product_url)
    soup = BeautifulSoup(web_page.content,'html.parser')
    headers = ["product_page_url","book_title","upc","price_including_tax","price_excluding_tax","quantity_available","description","category","review_rating","image_url"]
    #Column --> book_title 
    book_title = soup.find_all("li",class_="active")[0].text

    #for row in product_rows:
    table_headers = soup.find_all("th")
    header_values = soup.find_all("td")
    dict = {}
    #Columns --> upc,price_including_tax,price_excluding_tax,quantity_available
    for i in range(len(table_headers)):
        index = table_headers[i].text.strip()
        value = header_values[i].text.strip()
        dict[index] = value
    
    #Column --> description ## PENDING
    description =soup.find("article",class_="product_page").select("p")[3].get_text(strip=True)
    
    #Column --> category ## PENDING
    category = soup.find("ul",class_="breadcrumb").select("li")[2].find("a").get_text(strip=True)
    
    #Column --> review_rating
    rating = soup.find("article",class_="product_page").select("p")[2]
    review_rating = rating['class'][1]
    
    #Column --> image_url
    image_url =""
    images = soup.find_all("img")
    for im in images:
        if im['alt'] == book_title:
            image_url = im['src']
    image_url = image_url.replace("../..","http://books.toscrape.com/")
    
    with open('data.csv','w',newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(headers)
        data_row = [product_url,book_title,dict['UPC'],dict['Price (incl. tax)'],dict['Price (excl. tax)'],dict['Availability'],description,category,review_rating,image_url]
        writer.writerow(data_row)
    
def get_category_books_url(category_url):
    web_page = requests.get(category_url)
    soup = BeautifulSoup(web_page.content,'html.parser')

    category = soup.find("ul",class_="breadcrumb").select("li")[2].get_text(strip=True)
    print("Category: ",category)

    #count of books
    num_books = soup.find("form",class_="form-horizontal").select("strong")[0].get_text(strip=True)
    print("Total Books: ",num_books)
    
    list_of_book_urls = []
    i = 0
    book_sections = soup.find_all("article",class_="product_pod")  
    while i < int(num_books):
        book_url = book_sections[i].select("a")[1]["href"]    
        book_url = book_url.replace("../../..","http://books.toscrape.com/catalogue")
        list_of_book_urls.append(book_url)
        i += 1
    print(list_of_book_urls)


def menu():
    
    print("Phase 1: Press 1")
    print("Phase 2: Press 2")
    opt = int(input("Select option to execute phases:"))
    if opt == 1:
        get_product_details(URL)
    elif opt == 2:
        get_category_books_url(Category_URL)
    else:
        return 

menu()