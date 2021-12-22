import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
#chrome_options.add_argument('--headless')                          # Sans ecran
#chrome_options.add_argument('--no-sandbox')                        #
#chrome_options.add_argument('--disable-dev-shm-usage')             #

def buy_ldlc(link, LDLC_ACCOUNT, CARD):
    print('Commande de : {}'.format(link))
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(link)
    try:
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button color4 noMarge')]"))) # Cookie
        e.click();
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button picto color2 noMarge add-to-cart')]"))) # Ajouter au panier
        e.click();
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button color2 noMarge')]"))); # Voir le panier
        e.click();
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'account')]"))); # Account , pour ce connecter
        e.click();
        user = driver.find_element_by_name("Email")
        user.send_keys(LDLC_ACCOUNT['email'])
        pas = driver.find_element_by_name("Password")
        pas.send_keys(LDLC_ACCOUNT['password'])
        pas.submit()
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'basket')]"))); # Voir le pannier
        e.click();
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button maxi color2 noMarg')]"))) # Passer la commande
        e.click();
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'imgpayment img-cb')]"))) # Choisir le payement par carte
        e.click()
        time.sleep(1)
        num = driver.find_element_by_name("CardNumber")
        num.send_keys(CARD['num'])
        date = driver.find_element_by_name("ExpirationDate")
        date.send_keys(CARD['date'])
        name = driver.find_element_by_name("OwnerName")
        name.send_keys(CARD['name'])
        secret = driver.find_element_by_name("Cryptogram")
        secret.send_keys(CARD['secret'])
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button color2 maxi')]"))) # Passer la commande
        e.click();
        time.sleep(4)
        e = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(@class, 'title-1')]"))); # Check si la commande est passer
        merci = e.get_attribute("innerHTML")
        if "merci" in merci.lower():
            print('Achat effectué')
        else:
            print('Achat non-effectué')

    except Exception as e:
        print(e)


    driver.close();
    driver.quit();
    driver = None;
