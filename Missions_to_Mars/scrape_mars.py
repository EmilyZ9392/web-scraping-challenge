from splinter import Browser
from bs4 import BeautifulSoup as bs 
import pandas as pd
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_browser():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser= init_browser()
    mars_dict = {}

    # News scrape

    time.sleep(2)
    news_url= 'https://redplanetscience.com'
    browser.visit(news_url)
    html= browser.html
    news_soup = bs(html, 'html.parser')

    # Scrape latest title and teaser paragraph
    n_title = news_soup.find_all('div', class_='content_title')[0].text
    n_paragraph = news_soup.find_all('div', class_="article_teaser_body")[0].text

    # Scrape featured image
    time.sleep(2)
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    html= browser.html
    jpl_soup = bs (html,'html.parser')

    # Retrieve featured image link
    relative_image_path = jpl_soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = jpl_url + relative_image_path

    #Scrape facts, convert to html table
    facts_url = 'https://galaxyfacts-mars.com'
    table_df = pd.read_html(facts_url)[1]
    html_table = table_df.to_html()

    #Scrape hemisphere image and name
    time.sleep(2)
    hems_url = 'https://marshemispheres.com/'
    browser.visit(hems_url)
    hems_html = browser.html
    hems_soup = bs(hems_html, 'html.parser')

    all_hems= hems_soup.find('div', class_='collapsible results')
    mars_hems = all_hems.find_all('div', class_='item')
    hems_img_urls = []

    #loop through hemispheres to get title and images

    for i in mars_hems:
        ##title
        hemisphere = i.find('div', class_='description')
        title = hemisphere.h3.text
    
        ##full res img
        hems_img = hemisphere.a['href']
        browser.visit(hems_url + hems_img)
    
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
    
        img_link = img_soup.find('div', class_='downloads')
        img_url = img_link.find('li').a['href']
    
        ##dictionary
        img_dict = {
            'Title': title, 
            'Image': img_url
        }
        hems_img_urls.append(img_dict)

    #Mars Dictionary

    mars_dict = {
        'news_title': n_title, 
        'news_p': n_paragraph, 
        'featured_image_url' : featured_image_url,
        'fact_table': str(html_table),
        'hemisphere_image_urls': hems_image_urls
    }

    return mars_dict








