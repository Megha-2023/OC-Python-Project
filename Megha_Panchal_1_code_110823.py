"""Code to extract book details from Books to Scrape website """
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

#Column --> product_page_url
URL = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
Category_URL = "http://books.toscrape.com/catalogue/category/books/classics_6/index.html"           # url for category whose books are on single page
Multipage_Category_URL = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"  # url for category whose books are on multiple pages

def get_product_details(product_url):
    """Function to get all detailsl of speicified product url"""

    web_page = requests.get(product_url)
    soup = BeautifulSoup(web_page.content,'html.parser')
    dictofdetails = {"product_page_url":"","book_title":"","upc":"","price_including_tax":"","price_excluding_tax":"","quantity_available":"","description":"","category":"","review_rating":"","image_url":""}
    dictofdetails["product_page_url"] = product_url
    #Column --> book_title 
    book_title = soup.find_all("li",class_="active")[0].text
    dictofdetails["book_title"] = book_title
    #for row in product_rows:
    table_headers = soup.find_all("th")
    header_values = soup.find_all("td")
    dict = {}
    #Columns --> upc,price_including_tax,price_excluding_tax,quantity_available
    for i in range(len(table_headers)):
        index = table_headers[i].text.strip()
        value = header_values[i].text.strip()
        dict[index] = value

    dictofdetails["upc"] = dict["UPC"]
    dictofdetails["price_including_tax"] = dict["Price (incl. tax)"]
    dictofdetails["price_excluding_tax"] = dict["Price (excl. tax)"]
    dictofdetails['quantity_available'] = dict["Availability"]
    
    #Column --> description ## PENDING
    description =soup.find("article",class_="product_page").select("p")[3].get_text(strip=True)
    dictofdetails["description"] = description

    #Column --> category ## PENDING
    category = soup.find("ul",class_="breadcrumb").select("li")[2].find("a").get_text(strip=True)
    dictofdetails["category"] = category

    #Column --> review_rating
    rating = soup.find("article",class_="product_page").select("p")[2]
    review_rating = rating['class'][1]
    dictofdetails["review_rating"] = review_rating

    #Column --> image_url
    image_url =""
    images = soup.find_all("img")
    for im in images:
        if im['alt'] == book_title:
            image_url = im['src']
    image_url = image_url.replace("../..","http://books.toscrape.com/")
    dictofdetails["image_url"] = image_url
    
    return dictofdetails
    
def get_category_books_url(category_url):
    """Function to get urls of all books from speicified category"""
    list_of_book_urls = []
    
    while True:
        web_page = requests.get(category_url)
        soup = BeautifulSoup(web_page.content,'html.parser')

        category = soup.find("ul",class_="breadcrumb").select("li")[2].get_text(strip=True)
        print("Category: ",category)

        # check books are distributed on multiple pages
        strong_tags = soup.find("form",class_="form-horizontal").select("strong")
        
        # total number of books in the category
        total_num_books = strong_tags[0].get_text(strip=True)
        if len(strong_tags) == 1:
            start_index = 0
            end_index = int(total_num_books)
        else:
            start_index = int(strong_tags[1].get_text(strip=True))
            end_index = int(strong_tags[2].get_text(strip=True))
        
        # retrieve each book's url on the page
        book_sections = soup.find_all("article",class_="product_pod")
        i = 0
        j = int(start_index)  
        print("Total Books: ",total_num_books,start_index,end_index)
        while j <= int(end_index):
            if i >= int(total_num_books):
                break
            book_url = book_sections[i].select("a")[1]["href"]
            book_url = book_url.replace("../../..","http://books.toscrape.com/catalogue")
            list_of_book_urls.append(book_url)
            j += 1
            i += 1
        
        #check if next page exists or not
        next_page = soup.select_one("li.next>a")
        if next_page:
            next_url = next_page.get('href')
            category_url = urljoin(category_url, next_url)
            print(category_url)
        else:
            break
    print(list_of_book_urls,len(list_of_book_urls))
        
def write_details_csv():
    """ function to write book data to the csv file """
    header = []
    data_row =[]
    # retrive all books urls for specific category
    book_urls = get_category_books_url(Category_URL)



    
    dict_product = get_product_details(book_urls[0])
    with open('new_file.csv','w',newline='') as file:
        writer = csv.writer(file,delimiter=';')
        for key,value in dict_product.items():
            header.append(key)
            data_row.append(value)
        writer.writerow(header)  
        writer.writerow(data_row)  
                
        i = 1
        while i < len(book_urls):
            data_row = []   
            dict_product = get_product_details(book_urls[i])
            for key in dict_product:
                data_row.append(dict_product[key])
            writer.writerow(data_row)
            i += 1  
           

def menu():
    print("Phase 1: Press 1")
    print("Phase 2 (Sinle page category): Press 2")
    print("Phase 2 (Multipage Category): Press 3")
    opt = int(input("Select option to execute phases:"))
    if opt == 1:
        get_product_details(URL)
    elif opt == 2:
        get_category_books_url(Category_URL)
    elif opt == 3:
        get_category_books_url(Multipage_Category_URL)
    else:
        return 
    
menu()

