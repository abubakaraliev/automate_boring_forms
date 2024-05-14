from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from tqdm import tqdm
from pandas import read_csv

df = read_csv("data.csv")

FORM_URL = "https://careers.thalesgroup.com/fr/fr/apply?jobSeqNo=TGPTGWGLOBALR0247828EXTERNALFRFR&source=WORKDAY&step=1"


def fill_form_with_data(browser, entry):
    print("Filling form with data...")
    # print("Browser:", browser)
    
    wait = WebDriverWait(browser, 10)

    try:
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Accepter']")))
        accept_button.click()
    except Exception as e:
        print("Error clicking accept button:", e)
        
    browser.find_element(By.ID, "sourceType").send_keys(
        entry['Comment avez-vous entendu parler de nous ?'])
    sleep(1)
    browser.find_element(By.ID, "applicantSource").send_keys(entry['Source'])
    browser.find_element(By.ID, "country").send_keys(entry['Pays'])
    browser.find_element(
        By.ID, "cntryFields.firstName").send_keys(entry['Prénom'])
    browser.find_element(By.ID, "cntryFields.lastName").send_keys(
        entry['Nom de famille'])
    browser.find_element(By.ID, "cntryFields.preferredName").send_keys(
        entry['J’ai un nom préféré'])
    browser.find_element(By.ID, "cntryFields.addressLine1").send_keys(
        entry['Nom et type de voie ou/ Adresse'])
    browser.find_element(By.ID, "cntryFields.regionReference").send_keys(
        entry['Département'])
    sleep(1)
    browser.find_element(
        By.ID, "cntryFields.cityReference").send_keys(entry['Ville'])
    sleep(2)
    browser.find_element(By.ID, "cntryFields.postalCode").send_keys(
        str(entry['Code postal']))
    browser.find_element(By.ID, "email").send_keys(
        entry['Adresse électronique'])
    browser.find_element(By.ID, "deviceType").send_keys(
        entry['Type d’appareil téléphonique'])
    browser.find_element(By.ID, "phoneWidget.countryPhoneCode").send_keys(
        entry['Indicatif téléphonique du pays'])
    browser.find_element(By.ID, "phoneWidget.phoneNumber").send_keys(
        str(entry['Numéro de téléphone']))
    # browser.find_element(By.ID ,"next").click()
    browser.find_element(By.ID, "privacyCheckBox").click()


def fill_form_from_dataframe(browser, df):
    print("Filling form from dataframe...")

    for i in df.index:
        entry = df.loc[i]
        fill_form_with_data(browser, entry)


def launch_browser_and_fill_form():
    print("Launching browser and filling form...")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless")
    # options.add_argument("disable-gpu")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(10)
    
    browser.get(FORM_URL)
    while True:
        sleep(5)
        fill_form_from_dataframe(browser, df)
        return browser

browser = launch_browser_and_fill_form()
