# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

#NASA MARS NEWS
# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "./chromedriver.exe"}
browser = Browser("chrome", **executable_path)

# Enter the NASA News Site to be scraped
def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

# Retrieve page with the requests module
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

# Parse Results HTML with BeautifulSoup
    try:
        slide_element = soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

# Scrape the NASA Mars News Site and collect the latest News Title
        news_title = slide_element.find("div", class_="content_title").get_text()
        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

#JPL MARS SPACE IMAGES
# Enter the JPL Featured Space to be scraped
def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

# Find the image URL for the current Featured Mars Image 
# Click on the Feautured Mars Image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

# Click on "More Info" Button
    browser.is_element_present_by_text("more info", wait_time=1)
    moreinfo_element = browser.find_link_by_partial_text("more info")
    moreinfo_element.click()

# Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    img = image_soup.select_one("figure.lede a img")

    try:
        img_url = img.get("src")
    except AttributeError:
        return None 

# Obtain base URL
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"
    return featured_image_url


#MARS WEATHER
# Enter the Mars Weather twitter to be scraped
def twitter_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

# Parse Results HTML with BeautifulSoup
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

# Enter the Mars Weather twitter to be scraped
    mars_weather_tweet = weather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })

# Search Within Tweet for <p> to obtain the Tweet Text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    return mars_weather


#MARS FACTS
# Visit the Mars Facts Site Using Pandas
def mars_facts():
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
# Convert the data to a HTML table string.
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)
    return df.to_html(classes="table table-striped")


#MARS HEMISPHERE
# Enter the Mars Hemisphere site to be scraped
def hemisphere(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    image_url = []

# Get a List of All the Hemispheres Links
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

# Iterate through each Hemisphere
        browser.find_by_css("a.product-item h3")[item].click()

# Find the Image URL string for the full resolution hemisphere image
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

# Get Hemisphere Title containing the hemisphere name
        hemisphere["title"] = browser.find_by_css("h2.title").text

# Append Hemisphere Object to Python dictionary
        image_url.append(hemisphere)

# Navigate Backwards
        browser.back()

# Show list that contains one dictionary for each hemisphere
    return image_url


# HELPER FUNCTION
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")

    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


#WEB SCRAPING BOT
def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())

