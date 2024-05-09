import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

#Global Variables
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def main(csv_filename='scraped_data.csv'):
    all_data = []
    websites = [
        ('Decrypt', scrape_decrypt),
        ('Blockworks', scrape_blockworks),
        ('CoinDesk', scrape_coindesk),
        ('U.Today', scrape_u_today),
        ('BeInCrypto', scrape_beincrypto)
    ]
    
    rows_added = {}  # Dictionary to store the number of rows added from each website
    
    for website_name, scrape_function in websites:
        rows_before = len(all_data)
        scrape_function(all_data)
        rows_added[website_name] = len(all_data) - rows_before
    
    columns = ['date_scraped', 'headline', 'source']
    df = pd.DataFrame(all_data, columns=columns)
    
    if os.path.isfile(csv_filename):
        df_existing = pd.read_csv(csv_filename)
        df = pd.concat([df_existing, df], ignore_index=True)
    
    df.to_csv(csv_filename, index=False)
    
    print(f"Data saved to {csv_filename}.")
    for source, count in rows_added.items():
        print(f"Rows added from {source}: {count}")

# Call main
main()