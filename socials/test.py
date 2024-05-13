from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import json
from tiktok_uploader.auth import AuthBackend

# Set up the Selenium webdriver (make sure you have the appropriate webdriver installed)
driver = webdriver.Chrome()  # For Chrome, you can use webdriver.Firefox() for Firefox

# Set up the authentication backend with the cleaned cookies file
auth_backend = AuthBackend(cookies="../config/cookies.txt")

# Authenticate the agent using the browser backend
driver = auth_backend.authenticate_agent(driver)

# Encode the query parameter
encoded_query = urllib.parse.quote("cars")

# Construct the URL with the encoded query
url = f"https://www.tiktok.com/search?q={encoded_query}"

# Navigate to the TikTok search page
driver.get(url)

# Wait for the search results to be loaded
wait = WebDriverWait(driver, 10)
search_results = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'div[class*="DivItemContainerForSearch"]')
    )
)

# Scrape the search results
scraped_results = []
target_results = 500  # Specify the desired number of results to scrape

while len(scraped_results) < target_results:
    # Scroll down to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust the wait time as needed

    # Find all the search result elements
    search_results = driver.find_elements(
        By.CSS_SELECTOR, 'div[class*="DivItemContainerForSearch"]'
    )

    # Extract the title and caption for each search result
    for result in search_results:
        if len(scraped_results) >= target_results:
            break

        try:
            title_element = result.find_element(
                By.CSS_SELECTOR, "div.tiktok-1wrhn8t-DivContainer span"
            )
            title = title_element.text.strip()

            caption_element = result.find_element(
                By.CSS_SELECTOR, "div.tiktok-1ejylhp-DivContainer span"
            )
            caption = caption_element.text.strip()

            scraped_results.append({"title": title, "caption": caption})
        except:
            continue

# Save the scraped results to a JSON file
with open("scraped_results.json", "w", encoding="utf-8") as file:
    json.dump(scraped_results, file, ensure_ascii=False, indent=4)

# Close the webdriver
driver.quit()

print(f"Scraped {len(scraped_results)} results and saved them to scraped_results.json.")
