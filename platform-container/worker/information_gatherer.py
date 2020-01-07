import os
import requests
import hashlib
import csv,re,json,time,sys
from dateutil import parser
from bs4 import BeautifulSoup
from bs4 import Comment
from datetime import datetime
import traceback
import urllib.parse
import asyncio
import functools

from dataaccess import articles, article_sources

news_source = [
    {
        'source': 'npr',
        'url': 'https://www.npr.org/sections/politics/',
        'link_selector': 'div.item-info-wrap h2.title a',
        'time_selector': 'section time',
        'title_selector': 'div h1',
        'content_selector': 'div.storytext.storylocation.linkLocation',
        "enabled": True
     },
    {
        'source' : 'nymag',
        'url':'http://nymag.com/intelligencer/',
        'link_selector': 'div.feed-container a.feed-item.article',
        'time_selector': 'header time',
        'title_selector': 'h1.headline-primary',
        'content_selector': 'section.body p',
        "enabled": True
    },
    {
        'source': 'cnn',
        'url':'https://edition.cnn.com/specials/last-50-stories',
        'link_selector': 'h3.cd__headline a',
        'time_selector': 'p.update-time',
        'title_selector': 'h1.pg-headline',
        'content_selector': 'div.l-container div.pg-rail-tall__wrapper div.l-container .zn-body__paragraph',
        "enabled": True
    },
    {
        'source': 'politico',
        'url':'https://www.politico.com/news/2020-elections',
        'link_selector': 'section h1 a',
        'time_selector': 'section time',
        'title_selector': 'h2.headline',
        'content_selector': 'section div.story-text p',
        "enabled": True
    }
]


def generate_hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def find_links(dct):
    """
    This Function is used to find the links in a given site
    :param dct:
    :return:
    """

    # Extract information
    url = dct['url']
    link_selector = dct['link_selector']

    # details = dct['LINKS']
    # Checker = dct['Checker']
    # Use headers to pass the authentication
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # Request the page
    page = requests.get(url, headers=headers)
    # Parsing
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract links
    links = []
    base_url = urllib.parse.urljoin(url, '.')
    for a in soup.select(link_selector):
        print(a.get('href'))
        links.append(urllib.parse.urljoin(base_url, a.get('href')))

    return links

    # # Extracting the news links
    # for data in soup.find_all(details['div'], class_=details['class']):
    #     for a in data.find_all('a'):
    #         link = a.get('href')
    #         # This exception for CNN blog only
    #         if dct['Checker'] == 'https://edition.cnn.com/':
    #             link = 'https://edition.cnn.com{}'.format(link)
    #         # This for all blogs
    #         if link != None and link not in links and link.startswith(Checker):
    #             links.append(link)
    # # Links Found
    # print("FOUND {} LINKS IN THIS PAGE ...".format(len(links)))
    # return links


def scrape_page(link, dct):
    """
    This Function is used to extract the page information and format it into a dictionary object
    :param link:
    :param dct:
    :return:
    """

    # Request the page
    page = requests.get(r'{}'.format(link))

    # HTML Parser
    soup = BeautifulSoup(page.content, 'html.parser')

    # Loading page information
    # time_details = dct['TIME'] # Article datetime
    # title_details = dct['TITLE'] # Article title
    # content_details = dct['CONTENT'] # Article content

    time_selector = dct["time_selector"]
    title_selector = dct["title_selector"]
    content_selector = dct['content_selector']

    # Get formated date
    #date = re.search(r'\w* \d*, \d\d\d\d', time).group(0)

    # Extract required information
    time_elements = soup.select(time_selector)
    if len(time_elements) > 0:
        article_date = time_elements[0].get('datetime')
        if article_date is None:
            article_date = time_elements[0].text
    else:
        # default to today
        article_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Title
    article_title = ''
    title_elements = soup.select(title_selector)
    if len(title_elements) > 0:
        article_title = title_elements[0].get_text()

    #time = soup.find(time_details['div'], class_=time_details['class']).text
    #title = soup.find(title_details['div'], class_=title_details['class']).text

    # Get the article body content
    article_content = ''
    # for data in soup.find_all(content_details['div'], class_=content_details['class']):
    #
    #     if content_details['pc'] is not None:
    #         for p_data in data.find_all(content_details['p'], class_=content_details['pc']):
    #             # Remove unwanted tags
    #             [x.extract() for x in data.find_all('script')]
    #             [x.extract() for x in data.find_all('style')]
    #             [x.extract() for x in data.find_all('meta')]
    #             [x.extract() for x in data.find_all('noscript')]
    #             [x.extract() for x in data.find_all('div', class_="image")]
    #             [x.extract() for x in data.find_all(text=lambda text: isinstance(text, Comment))]
    #
    #             # Extract content text
    #             content = data.get_text()
    #             content = content.replace('\r', ' ').replace('\n', ' ')
    #             # content = " ".join(content.split())
    #             article_content += content + ' '
    #     else:
    #         # Remove unwanted tags
    #         [x.extract() for x in data.find_all('script')]
    #         [x.extract() for x in data.find_all('style')]
    #         [x.extract() for x in data.find_all('meta')]
    #         [x.extract() for x in data.find_all('noscript')]
    #         [x.extract() for x in data.find_all('div', class_="image")]
    #         [x.extract() for x in data.find_all(text=lambda text: isinstance(text, Comment))]
    #
    #         # Extract content text
    #         content = data.get_text()
    #         content = content.replace('\r', ' ').replace('\n', ' ')
    #         #content = " ".join(content.split())
    #         article_content += content + ' '

    # Extracted data

    for data in soup.select(content_selector):

        # Remove unwanted tags
        [x.extract() for x in data.find_all('script')]
        [x.extract() for x in data.find_all('style')]
        [x.extract() for x in data.find_all('meta')]
        [x.extract() for x in data.find_all('noscript')]
        [x.extract() for x in data.find_all('div', class_="image")]
        [x.extract() for x in data.find_all(text=lambda text: isinstance(text, Comment))]

        # Extract content text
        content = data.get_text()
        content = content.replace('\r', ' ').replace('\n', ' ')
        article_content += content + ' '

    article = {
        "id": generate_hash(link),
        "article_link": link,
        "article_date": article_date,
        "article_title": article_title,
        "article_content": article_content
    }

    return article


def gather_news_articles(dct):
    """
    This Function is used to Automate the process of news feed scrapping
    :param dct:
    :return:
    """

    # Find the links
    links = find_links(dct)
    # Find the data in each link
    for link in links:
        print(link)
        try:
            # Scrap the page
            article = scrape_page(link, dct)
            print(article)
            print("********")

            try:
                date_obj = parser.parse(article["article_date"])
            except:
                date_obj = parser.parse(article["article_date"][-17:])

            print(date_obj.timestamp())

            if (article["article_title"] != '') and (article["article_content"] != ''):
                # Save the news article
                articles.create(id=article["id"],
                                source=dct["source"],
                                article_link=article["article_link"],
                                article_date=article["article_date"],
                                article_title=article["article_title"],
                                article_content=article["article_content"],
                                article_dts=date_obj.timestamp())

        except Exception as e:
            print(link)
            print(e)
            print(traceback.format_exc())

def run():
    # Get the article sources
    loop = asyncio.get_event_loop()
    news_list = loop.run_until_complete(article_sources.browse())
    print(news_list)
    for source in news_list:
        if source["enabled"]:
            gather_news_articles(source)

if __name__ == "__main__":
    run()
    # for source in news_source:
    #     if source["enabled"]:
    #         gather_news_articles(source)
