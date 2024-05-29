from celery import shared_task
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import os
import time
from direction_backend.settings import env


@shared_task
def automatic_extract_jobs():
    url = env("URL")
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully render

        data = {visa: [] for visa in [
            '186', '189', '190', '494', '485', '407', '187',
            '491 state or territory nominated',
            '482 Medium term stream', '482 Short term stream',
            '489 state or territory nominated'
        ]}

        while True:
            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the table and extract data
            table = soup.find('table')
            if table is None:
                raise ValueError("Could not find the table on the webpage.")

            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_all('td')

                # Ensure we have enough cells in the row
                if len(cells) < 2:
                    continue

                occupation = cells[0].text.strip()

                # Get the visas from the nested <ul> list inside the second <td>
                visa_cell = cells[2] if len(cells) > 2 else cells[1]
                visas = visa_cell.find_all('li')

                for visa in visas:
                    visa_text = visa.text.strip()
                    for key in data:
                        if key in visa_text:
                            data[key].append(occupation)
                            break

            # Try to click the "Next" button to go to the next page
            try:
                next_button = driver.find_element(
                    By.XPATH, '//a[contains(@class, "next")]')
                if 'disabled' in next_button.get_attribute('class'):
                    break  # Exit loop if the next button is disabled
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                break  # Exit loop if no next button is found

        # Save data to text files
        output_dir = 'output_files'
        os.makedirs(output_dir, exist_ok=True)

        i = 1
        for visa, occupations in data.items():
            filename = os.path.join(
                output_dir, f'{i}_{visa.replace(" ", "_")}.txt')
            with open(filename, 'w') as f:
                for occupation in occupations:
                    f.write(f"{occupation}\n")
            i += 1

        return 'Scraping and saving completed successfully'

    finally:
        driver.quit()


def main():
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(automatic_extract_jobs, IntervalTrigger(
        minutes=env("EXTRACTION_REPEAT_TIME_MONTHS", cast=int))
    )
    scheduler.start()
