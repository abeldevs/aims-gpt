from dataclasses import dataclass
from bs4 import BeautifulSoup 
from numpy import asarray, savetxt
import numpy as np
import requests 

@dataclass
class ScrapperParams:
    url:str = 'https://aims.ac.za/'
    url_csv_path:str = 'data/url.csv'

class Scrapper:
    """
    Creating dataset using scrapping technique from the website
    ===========================================================
    Args:
       urls: List - used to collect all the urls from the root websites 
    
    """
    def __init__(self):
        self.__urls = []
        self.__paragraphs = []

    def get_urls(self):
        """
        To get all the sublinks found in the domains
        
        Args: 
            link: root domain link.
        Returns
            A list of links
        """
        # make the reuest to the root
        request = requests.get(ScrapperParams.url)
        # parse the item in the html
        parse = BeautifulSoup(request.text, 'html.parser')
        
        for item in parse.find_all('a'):
            # to remove irrelevant empty links and the link that contains pdf
            link = str(item.get('href'))
            if not link.__contains__('#') and not link.__contains__('.pdf') and not link.__contains__('None') and not link.__contains__('..'):
                self.urls = link

    def create_csv(self):
        """Converting the urls into csv files"""
        # get the urls
        self.get_urls()
        # saving the list of urls as csv
        savetxt(ScrapperParams.url_csv_path, self.urls, delimiter=',', fmt='%s')
    
    def scrap(self):
        """Enumerate through all links and get the paragraphs"""
        # get the site content
        for url in self.urls:
            request = requests.get(url) 
            # parsing the HTML 
            parse = BeautifulSoup(request.content, 'html.parser') 
            # get the content from the parsed html
            content = parse.find('div', class_='entry-content') 
            # find a paragraph item in the contentent
            paragraphs = content.find('p') 
            
            for par in paragraphs: 
                print(par.text)


    @property
    def urls(self): return self.__urls

    @urls.setter
    def urls(self, val): self.__urls.append(val)

    @property
    def paragraphs(self): return self.__paragraphs

    @urls.setter
    def paragraphs(self, val): self.__paragraphs.append(val)