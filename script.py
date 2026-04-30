import logging
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector
import json


# ---------------------- LOGGING SETUP ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ---------------------- DRIVER SETUP ----------------------
def setup_driver():
    logging.info("Initializing Chrome driver with anti-detection options")

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    return driver

def write_json(data, file_path, indent=4, ensure_ascii=False):
   
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

    logging.info(f"JSON written successfully → {file_path}")

# ---------------------- INSTALL EXTENSION ----------------------
def install_extension(driver):
    try:
        logging.info("Opening Chrome Web Store extension page")

        driver.get("https://chromewebstore.google.com/detail/free-ai-recaptcha-solver/iomcoelgdkghlligeempdbfcaobodacg")

        wait = WebDriverWait(driver, 15)

        add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Add to Chrome")]'))
        )
        add_button.click()

        logging.info("Clicked 'Add to Chrome' button")

        time.sleep(5)

        # Handle browser popup
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')

        logging.info("Confirmed extension installation popup")

        time.sleep(10)

    except Exception as e:
        logging.error(f"Extension installation failed: {e}")
        raise


# ---------------------- TRACK SHIPMENT ----------------------
def track_shipment(driver):
    try:
        logging.info("Navigating to tracking page")

        driver.get("https://www.saia.com/track")

        wait = WebDriverWait(driver, 15)

        # Select dropdown
        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "trackBy"))
        )
        Select(dropdown_element).select_by_value("Purchase Order Number")

        logging.info("Selected 'Purchase Order Number' in dropdown")

        # Input fields
        driver.find_element(By.ID, "trackByNumber").send_keys("P11182")
        driver.find_element(By.ID, "zip").send_keys("68117")

        logging.info("Entered tracking details")

        # Wait for captcha solve / delay
        logging.info("Waiting for captcha / page readiness")
        time.sleep(60)

        # Click track button
        track_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Track your shipment now"]'))
        )
        track_btn.click()

        logging.info("Clicked track button")

        time.sleep(3)

    except Exception as e:
        logging.error(f"Tracking step failed: {e}")
        raise


# ---------------------- SCRAPE TABLE ----------------------
def scrape_table(driver):
    try:
        logging.info("Parsing table data")

        sel = Selector(text=driver.page_source)

        theads = sel.xpath('//table[@class="table"]/thead/tr/th/text()').getall()
        items = {}
        for val in range(len(theads)):
            items[theads[val]] = sel.xpath(f'//table[@class="table"]/tbody/tr/td[{val+1}]/text()').get(default="").strip()

        return items

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        raise


# ---------------------- MAIN FLOW ----------------------
def main():
    driver = setup_driver()

    try:
        install_extension(driver)
        track_shipment(driver)

        data = scrape_table(driver)

        logging.info("Final Extracted Data:")
        
        if data:
            write_json(data, 'output.json')
            logging.info("data is saved to output.json")
        else:
            logging.info("No tracking details found")

    finally:
        logging.info("Closing driver")
        driver.quit()


if __name__ == "__main__":
    main()