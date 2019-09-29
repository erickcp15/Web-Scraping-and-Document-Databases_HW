from splinter import Browser
import pymongo
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    browser = init_browser()

    time.sleep(1)

    #Mars News

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.body.find('div', class_="content_title").text

    news_p = soup.body.find('div', class_="article_teaser_body").text

    #JPL Mars Space Images - Featured Image

    JPL__url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL__url)

    html = browser.html
    soup = bs(html, 'html.parser')

    stuff = soup.find('div', class_="carousel_container")

    img = stuff.a['data-fancybox-href']

    JPL_link = 'https://www.jpl.nasa.gov'
    featured_image_url = JPL_link + img

    #Mars Weather

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    tables =  pd.read_html(facts_url)

    mars_facts = tables[1]
    mars_facts.columns = ['description', 'value']
    mars_facts.set_index('description', inplace=True)
    mars_html = mars_facts.to_html()
    mars_html.replace('\n', '')

    #Mars Hemispheres

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    prod_results = soup.find('div', class_="collapsible results")

    hemispheres = prod_results.find_all('a')

    hemisphere_image_urls = []
    for hemi in hemispheres:
        if hemi.h3:
            title = hemi.h3.text
            link = hemi['href']
            test_url = 'https://astrogeology.usgs.gov/'
            two_link = test_url+link
            browser.visit(two_link)
            html = browser.html
            soup = bs(html, 'html.parser')
            stuff = soup.find('div', class_="downloads")
            img = stuff.ul.a['href']
            hemisphere_dict = {}
            hemisphere_dict['title'] = title
            hemisphere_dict['img_url'] = img
            hemisphere_image_urls.append(hemisphere_dict)
            browser.back()


    mars_py_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image":featured_image_url,
        "weather":mars_weather,
        "facts":mars_html,
        "hemispheres":hemisphere_image_urls
    }
    browser.quit()

    return mars_py_dict

