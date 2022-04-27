from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import date
import re
import json

class Crawler:
    def __init__(self):
        self.PATH = 'https://books.toscrape.com/'

        # driver setup
        chrome_options = Options()
        chrome_options.add_argument('--headless') # absolutely needed or chrome crashes
        s = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s,options=chrome_options)
        self.driver.get(self.PATH+'index.html')
        #self.driver.implicitly_wait(0.5)

        # full HTML page
        page = BeautifulSoup(self.driver.page_source,'html.parser')
        # sidebar with the categories
        element_categories_sidebar = page.find('ul',{'class': 'nav nav-list'})
        self.categories={}
        for line in element_categories_sidebar.find_all('a'):
            cat = line.get_text()
            cat = cat.replace('\n','')
            cat = cat.replace('  ','')
            self.categories[cat] = line.get('href').replace('index.html','')
        # 'Books' is also in the list
        self.categories.pop('Books')

    # Returns a dictionary with all books in the categories
    # cat: category
    def crawl(self, cat: str):
        books_data=[]

        doc = 'index.html'
        while True:
            path = self.PATH + self.categories[cat]
            
            # getting the element with books from the page
            self.driver.get(path + doc)
            page_c = BeautifulSoup(self.driver.page_source,'html.parser')
            element_book_list = page_c.find('ol',{'class': 'row'})

            # separating each book element
            books=[]
            for b in element_book_list.find_all('h3'):
                books.append(b.find('a').get('href'))

            # getting the data from each book element
            for b in books:
                self.driver.get(path + b)
                page_b = BeautifulSoup(self.driver.page_source,'html.parser')

                # element with the info itself
                element_main = page_b.find('article',{'class': 'product_page'})

                title = element_main.find('h1').text
                
                price = element_main.find('p',{'class': 'price_color'}).text
                price = float(price[1:])

                stock = 0
                try:
                    stock = element_main.find('p',{'class': 'instock availability'}).text
                    stock = int(re.findall('\d+',stock)[0])
                except:
                    pass
                
                # element with description
                desc = page_b.find('meta',{'name': 'description'}).get('content')
                desc = desc.replace('\n','')
                desc = desc.replace('  ','')

                day = date.today().strftime('%Y-%m-%d')

                book = {
                    'Título':title,
                    'Categoria':cat,
                    'Preço':price,
                    'Estoque':stock,
                    'Descrição':desc,
                    'Data de crawleamento':day,
                }

                books_data.append(book)
            
            # finding the next page button if it exists
            next_element = page_c.find('li',{'class': 'next'})
            if next_element == None:
                break
            doc = next_element.find('a').get('href')

        return books_data