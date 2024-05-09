import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

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

def scrape_decrypt(csv_filename='scraped_data.csv'):
    print("Starting Decrypt scrape...")
    url = "https://decrypt.co/"
    soup = fetch_and_parse(url)
    if soup:
        print("Webpage successfully fetched.")
        headline_containers = soup.find_all('div', class_='mt-0')
        columns = ['date_scraped', 'headline', 'source']
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for container in headline_containers:
            headline_anchor = container.find('a', class_='flex gap-2 items-start')
            headline_text = headline_anchor.get_text().strip() if headline_anchor else "No headline found"
            data.append([now, headline_text, url])

        df = pd.DataFrame(data, columns=columns)
        if os.path.isfile(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            df = pd.concat([df_existing, df], ignore_index=True)
        try:
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}. Rows added: {len(data)}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
    else:
        print("Failed to retrieve the webpage.")

def scrape_blockworks(csv_filename='scraped_data.csv'):
    print("Starting Blockworks scrape...")
    url = "https://blockworks.co/category/markets"
    soup = fetch_and_parse(url)
    if soup:
        print("Webpage successfully fetched.")
        headline_containers = soup.find_all('div', class_='flex flex-col justify-start self-stretch flex-grow gap-2 w-full')
        columns = ['date_scraped', 'headline', 'source']
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for container in headline_containers:
            headline_element = container.find('div', class_='flex justify-start items-start self-stretch flex-grow-0 flex-shrink-0 gap-2.5')
            headline_text = headline_element.get_text().strip() if headline_element else "No headline found"
            data.append([now, headline_text, url])

        df = pd.DataFrame(data, columns=columns)
        if os.path.isfile(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            df = pd.concat([df_existing, df], ignore_index=True)
        try:
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}. Rows added: {len(data)}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
    else:
        print("Failed to retrieve the webpage.")

def scrape_coindesk(csv_filename='scraped_data.csv'):
    print("Starting CoinDesk scrape...")
    url = "https://www.coindesk.com/"
    soup = fetch_and_parse(url)
    if soup:
        print("Webpage successfully fetched.")
        leaderboard_wrapper = soup.find('div', class_='defaultstyles__LeaderboardWrapper-sc-1hccfhf-0 kuxwiI')
        columns = ['date_scraped', 'headline', 'source']
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if leaderboard_wrapper:
            containers = leaderboard_wrapper.find_all('div')
            for container in containers:
                headline_anchor = container.find('div', class_='card-title')
                if headline_anchor:
                    headline_text = headline_anchor.get_text().strip() if headline_anchor else "No headline found"
                    data.append([now, headline_text, url])

        df = pd.DataFrame(data, columns=columns)
        if os.path.isfile(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            df = pd.concat([df_existing, df], ignore_index=True)
        try:
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}. Rows added: {len(data)}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
    else:
        print("Failed to retrieve the webpage.")

def scrape_u_today(csv_filename='scraped_data.csv'):
    print("Starting U.Today scrape...")
    url = "https://u.today/"
    soup = fetch_and_parse(url)
    if soup:
        print("Webpage successfully fetched.")
        headline_containers = soup.find_all('div', class_='news__item-title')
        columns = ['date_scraped', 'headline', 'source']
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for container in headline_containers:
            headline_text = container.get_text().strip() if container else "No headline found"
            data.append([now, headline_text, url])

        df = pd.DataFrame(data, columns=columns)
        if os.path.isfile(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            df = pd.concat([df_existing, df], ignore_index=True)
        try:
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}. Rows added: {len(data)}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
    else:
        print("Failed to retrieve the webpage.")

def scrape_beincrypto(csv_filename='scraped_data.csv'):
    print("Starting BeInCrypto scrape...")
    url = "https://beincrypto.com/"
    soup = fetch_and_parse(url)
    if soup:
        print("Webpage successfully fetched.")
        content_list = soup.find('ul', class_='unstyled-content-list')
        columns = ['date_scraped', 'headline', 'source']
        data = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if content_list:
            list_items = content_list.find_all('a', class_='block mb-1 font-semibold text-dark-grey-700 s2 s2--medium lg:s1 lg:s1--medium')
            for item in list_items:
                headline_text = item.get_text().strip() if item else "No headline found"
                data.append([now, headline_text, url])

        df = pd.DataFrame(data, columns=columns)
        if os.path.isfile(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            df = pd.concat([df_existing, df], ignore_index=True)
        try:
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}. Rows added: {len(data)}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
    else:
        print("Failed to retrieve the webpage.")

# Example of how to call the function
scrape_beincrypto('scraped_data.csv')
scrape_decrypt('scraped_data.csv')
scrape_blockworks('scraped_data.csv')
scrape_coindesk('scraped_data.csv')
scrape_u_today('scraped_data.csv')