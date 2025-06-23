import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Create the awards.csv file and write the header row
with open('awards.csv', mode='w', newline='') as awards_file:
    awards_writer = csv.writer(awards_file)
    awards_writer.writerow(["Title", "Total", "Winner", "Finalist", "Nominee"])

# Open the boardgames_ranks.csv file and read the rows
with open('boardgames_ranks.csv', mode='r') as ranks_file:
    ranks_reader = csv.reader(ranks_file)
    next(ranks_reader)  # Skip the header row

    CHROME_BIN_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    # Set up Selenium WebDriver (using Chrome in this example)
    service = Service(CHROME_BIN_PATH)  # Update with the path to your WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    for row in ranks_reader:
        game_id = row[0]
        game_name = row[1]

        # Get the web page
        url = f'https://boardgamegeek.com/boardgame/{game_id}'
        driver.get(url)

        # Wait for the <awards-module> element to be present
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'awards-module'))
            )
            awards_module = driver.find_element(By.TAG_NAME, 'awards-module')
            soup = BeautifulSoup(awards_module.get_attribute('outerHTML'), 'html.parser')

            total = 0
            winner = 0
            finalist = 0
            nominee = 0

            # Get the text of all "a" elements that are child elements of the awards-module
            for a in soup.find_all('a'):
                text = a.get_text().strip()
                total += 1
                if text.endswith("Nominee"):
                    nominee += 1
                elif text.endswith("Finalist"):
                    finalist += 1
                else:
                    winner += 1

            # Write the row to the awards.csv file
            with open('awards.csv', mode='a', newline='') as awards_file:
                awards_writer = csv.writer(awards_file)
                awards_writer.writerow([game_name, total, winner, finalist, nominee])

        except Exception as e:
            print(f"Error processing game {game_name} (ID: {game_id}): {e}")

        # Add a delay between requests to avoid overwhelming the server
        time.sleep(5)

    driver.quit()