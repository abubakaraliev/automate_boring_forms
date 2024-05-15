from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3926933609&f_AL=true&keywords=alternance%20tester&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R'
EMAIL = ''
PASSWORD = ''

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# options.add_argument("--headless")
# options.add_argument("disable-gpu")
driver.get(f"{URL}")

wait = WebDriverWait(driver, 10)

sleep(2)

accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]')))
accept_cookies_button.click()

sign_in_button = sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/nav/div/a[2]")))
sign_in_button.click()

email = driver.find_element(By.ID,"username")
email.send_keys(EMAIL)


password = driver.find_element(By.ID,"password")
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

all_listings = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
)

for listings in all_listings:

    try:
        listings.click()
    except StaleElementReferenceException:
        listings = driver.find_element(By.CSS_SELECTOR, ".job-card-container--clickable")
        listings.click()
    sleep(2)
    apply_button = driver.find_element(By.CSS_SELECTOR,".jobs-apply-button")
    apply_button.click()
    next_button = driver.find_element(By.CSS_SELECTOR,"footer button")
    next_button.click()
    sleep(2)
    next_button.click()
    review_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-button--primary")
    try:
        if review_button.get_attribute("data-control-name") == "continue_unify":
            next_button.click()
        else:
            close_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            close_button.click()
            sleep(2)
            discard_button = driver.find_element(By.ID, "ember440")
            discard_button.click()
            print("Complex application, skipped.")
            continue
        sleep(2)
        review_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-button--primary")
        if review_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            close_button.click()
            sleep(2)
            discard_button = driver.find_element(By.ID, "ember440")
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else :
            review_button.click()
            sleep(2)
            submit_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-button--primary")
            if submit_button.get_attribute("data-control-name") == "submit_unify":
                submit_button.click()
                sleep(2)
                discard_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
                discard_button.click()
                print("Complex application, skipped.")
                continue
    except NoSuchElementException:
        print("No application button, skipped.")
        continue