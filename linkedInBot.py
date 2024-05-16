from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3843956802&f_AL=true&keywords=alternance%20devops&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R'
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
print("Accepted cookies.")

sign_in_button = sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/nav/div/a[2]")))
sign_in_button.click()
print("Clicked on Sign In button.")

email = driver.find_element(By.ID,"username")
email.send_keys(EMAIL)
print("Entered email.")

password = driver.find_element(By.ID,"password")
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)
print("Entered password and pressed Enter.")

all_listings = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
print("All job listings loaded.")

for listings in all_listings:

    try:
        listings.click()
    except StaleElementReferenceException:
        listings = driver.find_element(By.CSS_SELECTOR, ".job-card-container--clickable")
        listings.click()
    print("Clicked on a job listing.")
    sleep(2)
    
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR,".jobs-apply-button")
    except NoSuchElementException:
        print("No apply button found, skipping this job listing.")
        continue
    
    apply_button.click()
    print("Clicked on Apply button.")
    next_button = driver.find_element(By.CSS_SELECTOR,"footer button")
    next_button.click()
    print("Clicked on Next button.")
    sleep(2)
    review_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-button--primary")
    try:
        if review_button.get_attribute("data-control-name") == "continue_unify":
            next_button.click()
            print("Clicked on Next button.")
        else:
            close_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            close_button.click()
            sleep(2)
            try:
                discard_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
                actions = ActionChains(driver)
                actions.move_to_element(discard_button).perform()

                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".artdeco-modal")))
                discard_button.click()
                print("Clicked on discard button.")
                
            except NoSuchElementException:
                print("No discard button found.")
                continue
            print("Complex application, skipped.")
            continue
        sleep(2)
        review_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-button--primary")
        if review_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            close_button.click()
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ember1236"]/span')))
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else :
            review_button.click()
            print("Clicked on Review button.")
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