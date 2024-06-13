import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_wikipedia(url):
    try:
        # Send a GET request to the Wikipedia URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize empty lists for countries and capitals
        countries = []
        capitals = []

        # Find the table containing data
        tables = soup.find_all('table', class_='wikitable')

        # We need to find the correct table with countries and capitals
        # In this case, the first table is what we need
        if tables:
            rows = tables[0].find_all('tr')

            # Iterate over each row in the table, skipping the header row
            for row in rows[1:]:
                columns = row.find_all(['th', 'td'])
                if len(columns) >= 2:
                    country = columns[0].get_text(strip=True)
                    capital = columns[1].get_text(strip=True)

                    countries.append(country)
                    capitals.append(capital)

            return countries, capitals
        else:
            print(f"No suitable table found on the page: {url}")
            return [], []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        return [], []

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []

def save_to_csv(data, filename):
    try:
        df = pd.DataFrame({'Country': data[0], 'Capital': data[1]})
        df.to_csv(filename, index=False)
        print(f"Scraping and saving complete. Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == '__main__':
    # URL of the Wikipedia page to scrape
    url = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
    
    # Scrape Wikipedia page for countries and capitals
    scraped_data = scrape_wikipedia(url)
    
    if scraped_data[0] and scraped_data[1]:
        # Specify the filename to save CSV
        filename = 'countries_and_capitals.csv'
        
        # Save data to CSV
        save_to_csv(scraped_data, filename)
    else:
        print('Scraping Wikipedia failed. No data to save.')
