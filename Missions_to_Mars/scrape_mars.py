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

    # hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_hems= soup.find('div', class_='collapsible results')
    mars_item= mars_hems.find_all('div', class_='item')
    hemisphere_image_urls = []

    #loop through hemispheres to get title and images

    for item in mars_item:
        try: 
        
            ##title
            hemisphere= item.find('div', class_='description')
            title = hemisphere.h3.text
    
            ##full res img
            hemisphere_url = hemisphere.a['href']
            browser.visit(url + hemisphere_url)

            html = browser.html
            img_soup= bs(html, 'html.parser')
            img_url = img_soup.find('li').a['href']
            full_url = url + img_url
            if (title and full_url):

                #print results
                print('-'*25)
                print (title)
                print(full_url)

            # hemisphere dict
        
            hemisphere_dict = {
                'title': title, 
                'img_url': full_url
            }
            hemisphere_image_urls.append(hemisphere_dict)
        except Exception as e:
            print(e)

    #Mars Dictionary

    mars_dict = {
        'n_title': n_title, 
        'n_paragraph': n_paragraph, 
        'featured_image_url' : featured_image_url,
        'fact_table': str(html_table),
        'hemisphere_images': hemisphere_image_urls
    }

    browser.quit()
    return mars_dict








