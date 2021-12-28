import time
from datetime import datetime
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')                          # Sans ecran
chrome_options.add_argument('--no-sandbox')                        #
chrome_options.add_argument('--disable-dev-shm-usage')             #

def buy_ldlc(link, LDLC_ACCOUNT, CARD, logger):
    logger.info('Commande de : {}'.format(link))
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

    driver.get(link)
    try:
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button color4 noMarge')]"))) # Cookie
        e.click();
        logger.info('Click cookie ok')
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button picto color2 noMarge add-to-cart')]"))) # Ajouter au panier
        e.click();
        logger.info('Click Ajouter au Panier ok')
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button color2 noMarge')]"))); # Voir le panier
        e.click();
        logger.info('Click Voir le panier ok')
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'account')]"))); # Account , pour ce connecter
        e.click();
        logger.info('Click account ok')
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email")))
        user.send_keys(LDLC_ACCOUNT['email'])
        pas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))
        pas.send_keys(LDLC_ACCOUNT['password'])
        logger.info('Formulaire login ok')
        pas.submit()
        logger.info('Submit connexion ok')
        e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'basket')]"))); # Voir le pannier
        e.click();
        logger.info('Click Voir le panier ok')
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button maxi color2 noMarg')]"))) # Passer la commande
        e.click();
        logger.info('Click Passer la commande ok')
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Non merci']|//span[contains(@class, 'imgpayment img-cb')]"))) # Choisir le payement par carte ou la garantie
        garantie = e.get_attribute("innerHTML")

        if 'non' in garantie.lower() and 'merci' in garantie.lower():
            logger.info("Garantie detecter")
            e.click()
            logger.info("Click Non merci garantie ok")
            e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'imgpayment img-cb')]"))) # Choisir le payement par carte
            e.click()
        else:
            e.click()

        logger.info('Click Payement par carte ok')
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "CardNumber")))
        num.send_keys(CARD['num'])
        date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "ExpirationDate")))
        date.send_keys(CARD['date'])
        name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "OwnerName")))
        name.send_keys(CARD['name'])
        secret = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Cryptogram")))
        secret.send_keys(CARD['secret'])
        logger.info('Formulaire carte ok')
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button color2 maxi')]"))) # Passer la commande
        e.click();
        logger.info('Click Passer la commande ok')
        driver.save_screenshot('capture_0_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        logger.info('En attente de la validation de la commande (5min max)')
        e = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Merci !']"))); # Check si la commande est passer
        merci = e.get_attribute("innerHTML")
        driver.save_screenshot('capture_1_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        if "merci" in merci.lower():
            logger.info('Achat effectué')
        else:
            logger.info('Achat non-effectué')

    except Exception as e:
        logger.info(e)
        logger.info('Achat non-effectué')
        driver.save_screenshot('capture_error_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        logger.info("ERROR Detecter, screenshot ok")


    driver.close();
    driver.quit();
    driver = None;
