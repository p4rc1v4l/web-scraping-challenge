##########################################
# Web Scraping Homework: Mission to Mars #
##########################################

# Import libraries and run configuration #
import pandas as pd
import requests
import time
import pymongo

from bs4 import BeautifulSoup as bs
from splinter import Browser


# Initialize browser #
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def persist_mars_data(mars_data):
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    mars_db = client.mars
    mission_data = mars_db.mission_to_mars
    mission_data.insert_one(
        mars_data
    )


def load_mars_data():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    mars_db = client.mars
    mission_data = mars_db.mission_to_mars
    return mission_data.find_one()


# NASA Mars News #
def get_nasa_mars_news():
    nasa_news_browser = init_browser()

    nasa_mars_news_url = 'https://mars.nasa.gov/news'
    nasa_news_browser.visit(nasa_mars_news_url)

    time.sleep(5)

    html = nasa_news_browser.html
    soup = bs(html, 'html.parser')

    news_gallery = soup.find('ul', class_='item_list')
    news_cards = news_gallery.find_all('li')

    news_title = news_cards[0].find('div', class_='content_title').text
    news_description = news_cards[0].find('div', class_='article_teaser_body').text

    nasa_news = {
        "news_title": news_title,
        "news_description": news_description
    }

    print(news_title)
    print(news_description)

    return nasa_news


# JPL Mars Space Images #
def get_jpl_mars_space_images():
    jpl_mars_space_images_browser = init_browser()

    jpl_mars_space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jpl_mars_space_images_browser.visit(jpl_mars_space_images_url)

    time.sleep(5)

    html = jpl_mars_space_images_browser.html
    soup = bs(html, 'html.parser')

    featured_image_article_element = soup.find('article', class_='carousel_item')
    image_name_element = featured_image_article_element.find('a', class_='button')
    partial_image_name = image_name_element['data-link']
    partial_image_name_parts = partial_image_name.split('=')
    image_name = partial_image_name_parts[1]

    featured_image_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/{image_name}_hires.jpg'

    print(featured_image_url)

    return featured_image_url


# Mars Weather #
def get_mars_weather():
    twitter_browser = init_browser()

    twitter_mars_weather_url = 'https://twitter.com/marswxreport'
    twitter_browser.visit(twitter_mars_weather_url)

    time.sleep(5)

    html = twitter_browser.html
    soup = bs(html, 'html.parser')

    twitter_card = soup.find(
        'div',
        class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'
    )

    mars_weather = twitter_card.find('span').text

    print(mars_weather)

    return mars_weather


# Mars Facts #
def get_mars_facts():
    tables = pd.read_html("https://space-facts.com/mars/")
    table_df = tables[0]
    table_df = table_df.rename(columns={0: "Fact", 1: "Value"})

    mars_facts_table = table_df.to_html(index=False, justify='center')

    print(mars_facts_table)

    return mars_facts_table


# Mars Hemispheres #
def get_mars_hemisphere():
    mars_hemispheres_browser = init_browser()

    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_hemispheres_browser.visit(mars_hemispheres_url)

    time.sleep(10)

    html = mars_hemispheres_browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_='collapsible results')
    items_list = results.find_all('div', class_='item')

    mars_hemispheres = []

    for item in items_list:
        link_element = item.find('a', class_='itemLink product-item')
        image_link = link_element['href']
        full_link = "https://astrogeology.usgs.gov" + image_link

        response = requests.get(full_link)
        soup = bs(response.text, 'html.parser')
        content_section = soup.find('section', class_='block metadata')
        title = content_section.find('h2').text

        downloads_element = soup.find('div', class_='downloads')
        images_links = downloads_element.find_all('a')
        link_to_full_hemisphere_pic = images_links[0]['href']

        title_and_image = {
            "title": title,
            "image_url": link_to_full_hemisphere_pic
        }

        mars_hemispheres.append(title_and_image)

    print(mars_hemispheres)

    return mars_hemispheres


# Execute scraping #
def scrape():
    scrape_data = {
        "nasa_mars_news": get_nasa_mars_news(),
        "jpl_mars_space_images": get_jpl_mars_space_images(),
        "mars_weather": get_mars_weather(),
        "mars_facts": get_mars_facts(),
        "mars_hemisphere": get_mars_hemisphere()
    }

    return scrape_data


# scrape()
