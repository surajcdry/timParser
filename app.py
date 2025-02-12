from bs4 import BeautifulSoup
import requests
import csv

page = 0

# opening/creating csv file to write the data
csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)

# creating heading row
csv_writer.writerow(['date', 'headline', 'link to listen'])
counter = 0
wanted = int(input("Posts wanted: "))

def parser():
    global counter
    global wanted
    global page

    # grabbing single article one after another
    source = requests.get(f'https://tim.blog/page/{page}').text
    soup = BeautifulSoup(source, 'lxml')
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

        counter += 1

        # if wanted number of posts is reached, break the loop
        if counter == wanted:
            break

        # write parsed data to the cms_scrape.csv file
        csv_writer.writerow([date, headline, listen_link])

while counter < wanted:
    page +=1
    parser()

csv_file.close()