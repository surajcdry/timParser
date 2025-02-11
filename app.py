from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://tim.blog/').text
soup = BeautifulSoup(source, 'lxml')

# opening/creating csv file to write the data
csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)

# creating heading row
csv_writer.writerow(['date', 'headline', 'link to listen'])


# grabbing single article one after another
for article in soup.find_all('article'):
    
    headline = article.h3.text
    date = article.find('time', class_='entry-date published').text

    # if podcast link not found (for example if simply a blog post), making sure the program doesn't break
    try:
        listen_link = article.find('a', class_='podcast-block__link')['href']
    except:
        listen_link = "Not Found"

    # print parsed data in terminal
    print("Date: " + date)
    print("Title: " + headline)
    print("Link to listen: " + listen_link)
    print()

    # write parsed data to the cms_scrape.csv file
    csv_writer.writerow([date, headline, listen_link])

csv_file.close()