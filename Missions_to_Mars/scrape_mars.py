# Import dependancies
from bs4 import BeautifulSoup
import requests
import pymongo
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def scrape_mars_info():
    ##############################
    # Featured Mars Article
    ##############################

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL for Mars News page
    url = "https://redplanetscience.com/#"

    # Visit Mars News page in browser, wait for all content to generate
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    # Create BS object and parse it
    soup = BeautifulSoup(html, "lxml")

    # Get most recent article title
    content_title = soup.find('div', class_='content_title').text

    # Get most recent article teaser text
    content_teaser = soup.find('div', class_='article_teaser_body').text

    ##############################
    # Featured Mars Image
    ##############################

    # Mars Images URL
    url2 = "https://spaceimages-mars.com/"

    # Visit Mars Images page in browser, wait for content to generate
    browser.visit(url2)
    time.sleep(1)
    html2 = browser.html

    # Create BS object and parse it
    soup = BeautifulSoup(html2, "lxml")

    # Get featured image url
    f_mars_img = soup.find('img', {'class': ['headerimage','fade-in']})['src']
    mars_img_url = f'{url}{f_mars_img}'

    ##############################
    # Mars Facts
    ##############################

    # Get Mars Facts URL
    url3 = "https://galaxyfacts-mars.com/"

    # Read Mars Stats Table with Pandas
    mars_stats = pd.read_html(url3)

    # Create df 
    mars_df = mars_stats[0]

    # Cleaning df
    # Make first row the table headers
    header = mars_df.iloc[0]
    mars_df = mars_df[1:]
    mars_df.columns = header

    # Make 'Mars - Earth Comparison' column the index
    mars_df.set_index('Mars - Earth Comparison', inplace=True)

    # Convert mars_df to html table for use later
    mars_facts_table = mars_df.to_html()


    ##############################
    # Mars Hemispheres
    ##############################

    # Mars Hemispheres URL
    url4 = "https://marshemispheres.com/"

    # Visit Mars Hemispheres page in browser, wait for all content to generate
    browser.visit(url4)
    time.sleep(1)
    html4 = browser.html

    # Create BS object and parse it
    soup = BeautifulSoup(html4, "lxml")

    # Get div class description, which holds the links for the hemisphere pages
    results2 = soup.find_all('div', class_='description')

    # Create empty array to hold image urls
    hemisphere_imgs = []

    # Create array for hemisphere names
    hemisphere_names = ["Ceberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]

    for result in results2:
        
        # Find link to hemisphere page
        hem_page = result.find('a', class_='itemLink')['href']
        hem_page = f'{url4}{hem_page}'
        
        # Open hemisphere page in bs
        hem_response = requests.get(hem_page)
        soup2 = BeautifulSoup(hem_response.text, 'lxml')
        
        # Find and retrieve image url of hemisphere
        # Get the original .tif image, which is the second in the list (position 1)
        # Then, extract the link to the image
        hem_img_u = soup2.find_all('li')[0]
        hem_img = hem_img_u.find('a')['href']
        hem_img = f'{url4}{hem_img}'
        
        # Append hemisphere image link to hemisphere_imgs array
        hemisphere_imgs.append(hem_img)

    # Create dictionary 
    hemisphere_image_urls = [
        {"title": "Cerberus", "img_url": hemisphere_imgs[0]},
        {"title": "Schiaparelli", "img_url": hemisphere_imgs[1]},
        {"title": "Syrtis Major", "img_url": hemisphere_imgs[2]},
        {"title": "Valles Marineris", "img_url": hemisphere_imgs[3]}
    ]
    hemisphere_image_urls

    mars_data = {
        "f_article_title": content_title,
        "f_article_teaser": content_teaser,
        "first_img": mars_img_url,
        "mars_table": mars_facts_table,
        "mars_hemisphere_names": hemisphere_names,
        "mars_hemisphere": hemisphere_image_urls
    }
    
    browser.quit()

    return mars_data
    

