from audioop import mul
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re
import multiprocessing
import time

from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
ua = UserAgent()
userAgent = ua.random
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"user-agent={userAgent}")
chrome_options.headless = True
chrome_options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'

class Scraper():

    def __init__(self):
        self.urls = []
        self.titles = []
        self.headings = []
        self.links = []
        self.words = []
        self.final_dict = {}
        self.search_params = {}
    
    def start(self, urls):
        self.urls = urls
        self.main_function(urls)


    def get_page(self, url):
        try:
            print('start')
            driver = webdriver.Chrome(options=chrome_options)
            print('got driver')
            driver.get(url)
            print('got page')
            driver.implicitly_wait(10)
            page = driver.page_source
            print('got page')
            driver.close()
            return page, url
        except:
            print('get page failed')
            return None



    def get_soup(self, page, url,
                containers = [r'article',r'div',r'section'],
                class_containers = [r'main',r'content',r'body'],
                headings_list = [r'h1',r'h2',r'h3',r'h4',r'h5'],
                element_list = [r'b',r'strong',r'li',r'ul',r'p',r'span',r'tspan']):
        try:
            soup = BeautifulSoup(page, "html.parser")
            try: 
                self.titles.append(soup.title.string)
            except:
                pass
            print(f'title: {soup.title.string}')
            # get all relevant links
            url_links = []
            for link in soup.find_all('a'):
                if link.get('href'):
                    url_links.append(link.get('href'))
            url_links = pd.Series(url_links, name='links')
            link_filter = r'^http.*'
            try:
                domain = re.search(r'(?<=//)(w{0,3})(.*?)(?=(\..{2,3}/))',url)
                dname = rf'.*{domain.group(1)}.*'
                url_links = url_links.where((url_links.str.contains(link_filter))&~(url_links.str.contains(dname))).dropna(axis=0,how='all')
            except:
                url_links = url_links.where(url_links.str.contains(link_filter)).dropna(axis=0,how='all')
            for u in url_links:
                self.links.append(u)
            #try to find and get article or main body content
            classes = []
            for container in containers:
                for class_c in class_containers:
                    #find out if there are relevant classes to call
                    reg = re.compile(class_c)
                    for item in soup.find_all(container, class_=reg):
                        for c in item:
                            classes.append(item.get_attribute_list('class'))
            url_word_list = []
            url_headings_list = []
            if classes:
                for container in containers:
                    for c in classes:
                        body = soup.find(container, class_=c)
                        try:
                            for item in body.find_all(element_list):
                                for word in item.get_text().split(' '):
                                    if word and word != ' ':
                                        url_word_list.append(word)
                        except:
                            pass
                        try:
                            for item in body.find_all(headings_list):
                                for heading in item.get_text().split(' '):
                                    if heading and heading != ' ':
                                        url_headings_list.append(heading)
                        except:
                            pass
            for a in url_word_list:
                self.words.append(a)
            for b in url_headings_list:
                self.headings.append(b)
            print(f'finished parsing page')                                                   
        except:
            print('didnt parse')
            pass

    def main_function(self, urls):
        pool = multiprocessing.Pool(processes=len(urls))
        a = pool.imap_unordered(self.get_page,urls)
        self.final_dict = {}
        x = 1
        for element, url in a:
            self.final_dict[f'url #{x}'] = self.get_soup(element, url)
            x+=1

    def get_company_reddit(company, timeframe, limit, listing): 
        try:
            base_url = f'https://www.reddit.com/search.json?q={company}&limit={limit}&t={timeframe}&sort={listing}'
            request = requests.get(base_url, headers = {'User-agent': 'SimpleScraper'})
        except:
            print('An Error Occured')
        return request.json()

    def reddit_function(self, urls):
        pool = multiprocessing.Pool(processes=len(urls))
        a = pool.imap_unordered(self.get_page,urls)
        self.final_dict = {}
        x = 1
        for element, url in a:
            self.final_dict[f'url #{x}'] = self.get_company_reddit(element, url)
            x+=1


#         urls = ['https://markets.businessinsider.com/commodities/lumber-price',
#  'https://www.nasdaq.com/market-activity/commodities/lbs',
#  'https://tradingeconomics.com/commodity/lumber',
#  'https://www.nasdaq.com/market-activity/commodities/lbs']