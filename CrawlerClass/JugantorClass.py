#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from baseCralerClass import *
# import mysql.connector

class jugantorCrawler(NewsCrawler):
    def __init__(self):
        super().__init__(source_id = 2, source_name= 'Jugantor', base_url = 'https://www.jugantor.com/')
        
    def fetch_article(self, url):
        c=0
        try:
            source_code = requests.get(url)
        except:
            return
        pain_text = source_code.text
        soup = bs4.BeautifulSoup(pain_text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        for item_name in soup.findAll('div', {'class': 'headline_section'}):
            headLine=item_name.text
            #print(val1)
            c+=1    
        for item_name in soup.findAll('div', {'id': 'myText'}):
            itemBody=item_name.text
            #print(val2)
            c+=1
        itemDate=""    
        for item_name in soup.findAll('div', {'class': 'rpt_name'}):
            data = item_name.text.split(",")
            date = data[0].split(" ")
            #val3=date[0]
            it=len(date)
            for piece in date:
                #val3=piece
                if it<=3:
                    itemDate+=piece
                it-=1
    #        cpy_sheet.write(count, 1, item_name.text)
        try:
            if(c==2):
                return {
                    'timestamp'    : datetime.now(),
                    'url'          : url,
                    'article_date' : itemDate,
                    'article_title': headLine,
                    'article_body' : itemBody
                }
        except:
            return None
        '''
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = bs4.BeautifulSoup(plain_text, 'html.parser')

        header_items =  soup.findAll('h1', {'class': 'title mb10'})
        if len(header_items) > 0:
            article_title = header_items[0].text
        else: return None     

        article_bodies = soup.findAll('div', {'itemprop': 'articleBody'})
        if len(article_bodies) > 0:
            article_body = article_bodies[0].text
        else: return None

        date_published_items = soup.findAll('span', {'itemprop': 'datePublished'})
        if len(date_published_items) > 0:
            date_published = date_published_items[0].text
        else: return None

        return {
            'timestamp'    : datetime.now(),
            'url'          : url,
            'article_date' : date_published,
            'article_title': article_title,
            'article_body' : article_body
        }
        '''

    def fetch_all_articles(self, base_url = None):
        if base_url is None:
            base_url = self.base_url
        articles = []
        try:
            scraper = cloudscraper.create_scraper(
              interpreter='nodejs',
              recaptcha={
                'provider': 'anticaptcha',
                'api_key': '2930bf4ee0b441dc5ff61cb0c8060f76'
              }
            )
            source_code = scraper.get(base_url).text

        # any actions
        except AnticatpchaException as e:
            if e.error_code == 'ERROR_ZERO_BALANCE':
                #notify_about_no_funds(e.error_id, e.error_code, e.error_description)
                print(" ")
            else:
                raise
        #source_code = requests.get(url)
        plain_text = source_code
        soup2 = bs4.BeautifulSoup(plain_text, 'html.parser')
        for link in soup2.findAll('a'):
            #print(link.get('href'))
            try:
                st=link.get('href').split(":")
                if(st[0]=="https" or st[0]=="http"):
                    href=link.get('href')
                article = self.fetch_article(href)
                if article is not None:
                    articles.append(article)
                    print(co)
                    co=co+1;
                    print(article['article_title'])
                    print(article['article_body'])
            except:
                print("Problem in extraction...")
                
        return {
            'timestamp'    : datetime.now(),
            'base_url'     : base_url,
            'article_count': len(articles),
            'articles'     : articles
        }

