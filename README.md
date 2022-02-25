# This is a SEO keyword analysis project
---

The purpose of this is to allow you to type in a few keywords and receive a historgram of most used words. 

---

This project uses (in addtion to pandas, re, time, numpy, etc.): 

googlesearch: https://github.com/Nv7-GitHub/googlesearch

pytrends: https://github.com/GeneralMills/pytrends#related-topics

selenium: https://www.selenium.dev/

BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 

---

## If you'd like to use this notebook

    git clone https://github.com/camhendo/seo_topic_keywords.git

## You'll need a few things to make the webscraping word

- Chrome Driver for Chrome 99 (aka Chrome Beta)

Chrome Driver: https://chromedriver.chromium.org/downloads

*ensure this installed on your path* 

*if on a mac, use <code> brew install --cask chromedriver </code>*

Chrome Beta: https://www.google.com/intl/en_ca/chrome/beta/


# How to use

### Utilize the jupyter notebook to run functions one at a time or run them all in sequence

The total runtime of this jupyter takes 3 minutes at a minimum usually. The more keywords you add and the more results you want, the longer it will take.

If you find that you're getting blocked by domains, try to increase the sleep variable to ensure that requests are accepted by websites. 

---

### Finder Class
Initialize with the list of topics you're looking to analyze

Example initialization

    from searching import Finder
    ['topic 1', 'topic 2', topic 3',...,'topic n']
    finder_object = Finder(topics)
    finder_object.start_search()

    #to see the results
    finder_object.querieslist
    #or
    finder_object.url_list

Argument options for instantiating the search object (optional)

    Finder.start_search(
        category=0, # see a list of categories google topics uses here: https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
        timeframe='today 3-m', 
        geography='', 
        gprop='', 
        valuethreshhold = 50,
        num_results=5, 
        lang="en",
        sleep=3
    )

This function is used to figure out what queries you would like to search for on google. If you would like to bypass this function, you can fill a list with the queries you would like to search for and use Finder.search_queries(args)

    Finder.search_queries(
        queries, #-> list of query/queries you want to search for
        num_results, #-> how many results you want for each search (this usually set to 1, if you have many searches, consider keeping this number low)
        lang, #-> 2-letter language symbol to search in ('en') for english
        sleep #-> how long to sleep between searches (leaving this at 0 gives rise to the possibility that you get blocked so beware)
    )

---

### Scaper Class
This class does the bulk of the work for this project. It takes the resulting link list created by the Finder class and loads the links and uses bs4 to scrape them. 
This class uses multiprocessing and webdriver, to open and scrape a lot of websites simultaneously. 

Example init

    from multiprocess import Scraper
    the_scraper = Scraper()
    the_scraper.start(list_of_urls)


After this finishes, you can access an array of results

Page Titles (from "<title>" tag)
    the_scraper.titles

Anything inside header tags
    the_scraper.headings

Any links in body content that aren't to other places on the same site
    the_scraper.links

All words scraped from all searches
    the_scraper.words

If you would like to pull up results from a specific link
    the_scraper.final_dict

If you would like to adjust the search parameters, just add a dictionary that looks like the one below

    search_params = {
                    containers : [r'article',r'div',r'section'],
                    class_containers : [r'main',r'content',r'body'],
                    headings_list : [r'h1',r'h2',r'h3',r'h4',r'h5'],
                    element_list : [r'b',r'strong',r'li',r'ul',r'p',r'span',r'tspan']
    }

---

### The rest of the Jupyter file
The rest of the file is a analysis of the results that specifically pulls and looks at a histogram of words
If you find extraneous words, add them to the stoplist and they'll be excluded on the next time you run through the program. 
You can apply similar analysis to titles (will need to iterate through them one by one if you want a word list), to links (filter domains using a regex), or to headings.

Example domain-name regex = <code> r'(?<=//)(w{0,3})(.*?)(?=(\..{2,3}/)' </code>

Note: this might not catch all domains depending on complexity. 


Contact me:
Twitter: [@_camhendo](https://twitter.com/_camhendo)
