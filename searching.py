from googlesearch import search
import time
import pandas as pd
import numpy as np
from pytrends.request import TrendReq

class Finder:
    def __init__(self, topics):
        self.topics = topics
        self.querieslist = []
        self.url_list = []

    def start_search(self, category=0, timeframe='today 3-m', geography='', gprop='', valuethreshhold = 50, num_results=5, lang="en",sleep=3):
        self.get_google_queries(self.topics, category, timeframe, geography, gprop, valuethreshhold)
        queries = []
        for item in self.querieslist:
            for k, v in item.items():
               for q in v:
                    queries.append(q)
        return self.search_queries(queries, num_results, lang, sleep)

    def get_google_queries(self, topics, category, timeframe, geography, gprop, valuethreshhold):
        pytrends = TrendReq(hl='en_US', tz=360, backoff_factor=0.2)
        pytrends.build_payload(topics,cat=category,timeframe=timeframe,geo=geography,gprop=gprop)
        pytrends.interest_over_time()
        a = pytrends.related_queries()
        for x in range(0,len(topics)):
            topicdict = {}
            b = a[topics[x]]['top']
            try:
                c = b[b['value']> valuethreshhold]
                topicdict[topics[x]] = c['query'].to_list()
            except:
                topicdict[topics[x]] = ''
            self.querieslist.append(topicdict)

    def search_queries(self,queries,num_results,lang,sleep):
        for item in queries:
            s_obj = search(item, num_results=num_results, lang=lang)
            for item in s_obj:
                # for url in item:
                self.url_list.append(item)
            time.sleep(sleep)
        return self.url_list