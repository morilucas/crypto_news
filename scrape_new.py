import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

#Global Variables
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.now().strftime("%Y-%m-%d")

def fetch_and_parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def scrape_decrypt(data):
    url = "https://decrypt.co/"
    soup = fetch_and_parse(url)
    if soup:
        headline_containers = soup.find_all('div', class_='mt-0')
        for container in headline_containers:
            headline_anchor = container.find('a', class_='flex gap-2 items-start')
            headline_text = headline_anchor.get_text().strip() if headline_anchor else "No headline found"
            data.append([now, headline_text, url])

def scrape_blockworks(data):
    url = "https://blockworks.co/category/markets"
    soup = fetch_and_parse(url)
    if soup:
        headline_containers = soup.find_all('div', class_='flex flex-col justify-start self-stretch flex-grow gap-2 w-full')
        for container in headline_containers:
            headline_element = container.find('div', class_='flex justify-start items-start self-stretch flex-grow-0 flex-shrink-0 gap-2.5')
            headline_text = headline_element.get_text().strip() if headline_element else "No headline found"
            data.append([now, headline_text, url])

def scrape_coindesk(data):
    url = "https://www.coindesk.com/"
    soup = fetch_and_parse(url)
    if soup:
        leaderboard_wrapper = soup.find('div', class_='defaultstyles__LeaderboardWrapper-sc-1hccfhf-0 kuxwiI')
        if leaderboard_wrapper:
            containers = leaderboard_wrapper.find_all('div')
            for container in containers:
                headline_anchor = container.find('div', class_='card-title')
                if headline_anchor:
                    headline_text = headline_anchor.get_text().strip() if headline_anchor else "No headline found"
                    data.append([now, headline_text, url])

def scrape_u_today(data):
    url = "https://u.today/"
    soup = fetch_and_parse(url)
    if soup:
        headline_containers = soup.find_all('div', class_='news__item-title')
        for container in headline_containers:
            headline_text = container.get_text().strip() if container else "No headline found"
            data.append([now, headline_text, url])

def scrape_beincrypto(data):
    url = "https://beincrypto.com/"
    soup = fetch_and_parse(url)
    if soup:
        content_list = soup.find('ul', class_='unstyled-content-list')
        if content_list:
            list_items = content_list.find_all('a', class_='block mb-1 font-semibold text-dark-grey-700 s2 s2--medium lg:s1 lg:s1--medium')
            for item in list_items:
                headline_text = item.get_text().strip() if item else "No headline found"
                data.append([now, headline_text, url])

def scrape_cryptotimes(data):
    url = "https://www.cryptotimes.io/category/market-news/"
    soup = fetch_and_parse(url)
    if soup:
        containers = soup.find_all('div', class_='p-wrap p-list p-list-2')
        unique_headlines = set()  # To store unique headlines
        for container in containers:
            headline_elements = container.find_all('h3', class_='entry-title')
            for headline in headline_elements:
                headline_text = headline.get_text().strip() if headline else "No headline found"
                if headline_text not in unique_headlines:  # Check for duplicates
                    unique_headlines.add(headline_text)
                    data.append([now, headline_text, url])

def log_headline_counts(rows_added, log_filename='headline_counts.csv'):
    log_data = []
    for source, count in rows_added.items():
        log_data.append([today, source, count])
    
    columns = ['date', 'website', 'headline_count']
    if os.path.isfile(log_filename):
        df_existing = pd.read_csv(log_filename)
        df_new = pd.DataFrame(log_data, columns=columns)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = pd.DataFrame(log_data, columns=columns)
    
    df.to_csv(log_filename, index=False)

def main(csv_filename='scraped_data.csv', test_csv_filename='test_scraped_data.csv', test=False):
    all_data = []
    websites = [
        ('Decrypt', scrape_decrypt),
        ('Blockworks', scrape_blockworks),
        ('CoinDesk', scrape_coindesk),
        ('U.Today', scrape_u_today),
        ('BeInCrypto', scrape_beincrypto),
        ('CryptoTimes', scrape_cryptotimes)  # Add CryptoTimes to the list
    ]
    
    rows_added = {}  # Dictionary to store the number of rows added from each website
    
    for website_name, scrape_function in websites:
        rows_before = len(all_data)
        scrape_function(all_data)
        rows_added[website_name] = len(all_data) - rows_before
    
    columns = ['date_scraped', 'headline', 'source']
    df = pd.DataFrame(all_data, columns=columns)
    
    # Choose the appropriate CSV file based on the test flag
    filename = test_csv_filename if test else csv_filename
    
    if os.path.isfile(filename):
        df_existing = pd.read_csv(filename)
        df = pd.concat([df_existing, df], ignore_index=True)
    
    df.to_csv(filename, index=False)
    
    # Log the number of headlines extracted
    log_filename = 'test_headline_counts.csv' if test else 'headline_counts.csv'
    log_headline_counts(rows_added, log_filename)
    
    print(f"Data saved to {filename}.")
    for source, count in rows_added.items():
        print(f"Rows added from {source}: {count}")

# Call main for testing
main()