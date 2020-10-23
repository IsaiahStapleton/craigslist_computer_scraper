from requests import get
from bs4 import BeautifulSoup
import numpy as np
from random import randint
from time import sleep
import pandas as pd

response = get('https://charleston.craigslist.org/search/sya?')

soup = BeautifulSoup(response.text, "html.parser")

posts = soup.find_all('li', class_='result-row')

post_prices = []
post_dates = []
post_titles = []
post_links = []
post_towns = []

num_results = soup.find('div', class_='search-legend')
total_results = int(num_results.find('span', class_='totalcount').text)

pages = np.arange(0, total_results + 1, 120)


for page in pages:

    response = get('https://charleston.craigslist.org/search/sya?'
                   + 's=' + str(page))

    sleep(randint(1, 5))

    html = BeautifulSoup(response.text, 'html.parser')

    posts = html.find_all('li', class_='result-row')

    for post in posts:

        # Find prices
        single_price = post.find('span', class_='result-price').text
        post_prices.append(single_price)

        # Find dates
        single_date = post.find('time', class_='result-date')['datetime']
        post_dates.append(single_date)

        # Find titles
        single_title = post.find('a', class_='result-title hdrlnk').text
        post_titles.append(single_title)

        # Find links
        single_link = post.find('a', class_='result-title hdrlnk')['href']
        post_links.append(single_link)

        # Find towns
        if post.find('span', class_='result-hood') is not None:
            single_town = post.find('span', class_='result-hood').text
            post_towns.append(single_town)
        else:
            post_towns.append('NA')

result = pd.DataFrame({'Title': post_titles,
                       'Price': post_prices,
                       'Date': post_dates,
                       'Town': post_towns,
                       'Link': post_links})


writer = pd.ExcelWriter('computerData.xlsx')

result.to_excel(writer)

writer.save()

print("DataFrame was written successfully to Excel File")


