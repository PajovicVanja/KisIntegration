import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_nba_stats():
    # Set up Selenium with the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Define the URL of the NBA stats page
        url = 'https://www.nba.com/stats/leaders'

        # Use Selenium to open the page
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)  # This delay is to ensure that the page has loaded completely

        # Now that the page is loaded, you can parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the table with player stats
        table = soup.find('table', class_='Crom_table__p1iZz')
        players_stats_dict_list = []  # New list to hold player stats dictionaries

        # Check if the table was found
        if table:
            # Extract the headers
            headers = [header.get_text(strip=True) for header in table.find('thead').find_all('th')]

            # Find all table rows with stats in the body of the table
            for row in table.find('tbody').find_all('tr'):
                # Create a dictionary for each player's stats
                player_stats_dict = {}
                for header, cell in zip(headers, row.find_all('td')):
                    player_stats_dict[header] = cell.get_text(strip=True)
                players_stats_dict_list.append(player_stats_dict)

            # Return the list of player stats dictionaries
            return players_stats_dict_list
        else:
            print('Stats table not found. The page structure may have changed or content is loaded dynamically.')
            return None
    finally:
        # Close the Selenium browser
        driver.quit()
