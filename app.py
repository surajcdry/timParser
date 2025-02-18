from bs4 import BeautifulSoup
import requests
import csv

def fetch_page(page_num):
    """Fetch and parse a single page from Tim Ferriss blog"""
    url = f'https://tim.blog/page/{page_num}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return None

def parse_articles(soup, wanted_count):
    """Extract article data from the page"""
    articles = []
    
    for article in soup.find_all('article'):
        # Extract basic article info
        headline = article.h3.text
        date = article.find('time', class_='entry-date published').text
        
        # Get podcast link if available
        try:
            listen_link = article.find('a', class_='podcast-block__link')['href']
        except:
            listen_link = "Not Found"

        # Store article data
        articles.append([date, headline, listen_link])
        
        # Print article details
        print(f"Date: {date}")
        print(f"Title: {headline}")
        print(f"Link to listen: {listen_link}\n")
        
        if len(articles) >= wanted_count:
            break
            
    return articles

def save_to_csv(articles):
    """Save articles to CSV file"""
    with open('cms_scrape.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'headline', 'link to listen'])
        writer.writerows(articles)

def main():
    # Get user input
    wanted = int(input("Posts wanted: "))
    print()
    
    articles = []
    page = 1
    
    # Fetch articles until we have enough
    while len(articles) < wanted:
        soup = fetch_page(page)
        if not soup:
            break
            
        new_articles = parse_articles(soup, wanted - len(articles))
        articles.extend(new_articles)
        
        if not new_articles:  # No more articles found
            break
            
        page += 1
    
    # Save results
    save_to_csv(articles)
    print(f"\nSuccessfully saved {len(articles)} articles to cms_scrape.csv")

if __name__ == "__main__":
    main()