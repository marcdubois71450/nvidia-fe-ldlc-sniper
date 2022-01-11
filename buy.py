import time
import urllib

import requests

from random import randrange

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def buy_ldlc(link, LDLC_ACCOUNT, CARD, logger, driver):
    RESULT = False

    if '?' in link.split('/')[-1]:
        link = link + '&timestamp{}={}'.format(str(randrange(0, 9999)), str(time.time()).replace('.', ''))
    else:
        link = link + '?timestamp{}={}'.format(str(randrange(0, 9999)), str(time.time()).replace('.', ''))

    logger.info('Commande de : {}'.format(link))

    try:
        driver.get('https://www.ldlc.com/')
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button color4 noMarge')]"))) # Cookie
        e.click();
        logger.info('Click cookie ok')
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

        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/header/div[2]/div/div/div[2]/a/img"))) # Click Home logo
        e.click();
        logger.info('Click Home Logo ok')

        driver.get(link)
        logger.info('Load link ok')

        type_2 = 'none'
        try:
            e2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-page-price']/div[2]/button[2]")))
            if e2.is_displayed():
                text2 = e2.get_attribute("innerHTML")
                if 'ajouter' in text2.lower() and 'panier' in text2.lower():
                    type_2 = 'panier'

                elif 'acheter' in text2.lower() and 'article' in text2.lower():
                    type_2 = 'direct'

                else:
                    type_2 = 'none'

            else:
                type_2 = 'none'
        except:
            pass

        type_1 = 'none'
        try:
            e1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-page-price']/div[2]/button[1]")))

            if e1.is_displayed():
                text1 = e1.get_attribute("innerHTML")
                if 'ajouter' in text1.lower() and 'panier' in text1.lower():
                    type_1 = 'panier'

                elif 'acheter' in text1.lower() and 'article' in text1.lower():
                    type_1 = 'direct'

                else:
                    type_1 = 'none'
            else:
                type_1 = 'none'
        except:
            pass

        FAIL = True
        if type_1 == 'panier' or type_2 == 'panier':

            if type_1 == 'panier':
                e1.click();
            elif type_2 == 'panier':
                e2.click();


            logger.info('Click Ajouter au Panier ok')
            e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='modal-mise-panier']/div/div/div/div[1]/div[2]/div[3]/a"))); # Voir le panier
            e.click();
            logger.info('Click Voir le panier ok')
            e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='button maxi color2 noMarg']"))) # Passer la commande
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

            FAIL = False


        elif type_1 == 'direct' or type_2 == 'direct':

            if type_1 == 'direct':
                e1.click();
            elif type_2 == 'direct':
                e2.click();


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

            FAIL = False

        elif type_1 == 'none' or type_2 == 'none':
            logger.info("Erreur aucun bouton d'achat ok")
            driver.save_screenshot('capture_error_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
            with open('ldlc_none_error_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.html', "w") as f:
                f.write(driver.page_source)

            FAIL = True

        if not FAIL:
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
        #    e.click();
        #    logger.info('Click Passer la commande ok')
        #    driver.save_screenshot('capture_0_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        #    logger.info('En attente de la validation de la commande (5min max)')
        #    e = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Merci !']"))); # Check si la commande est passer
        #    merci = e.get_attribute("innerHTML")
        #    driver.save_screenshot('capture_1_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        #    if "merci" in merci.lower():
        #        logger.info('Achat effectué')
        #        RESULT = True
        #    else:
        #        logger.info('Achat non-effectué')
        #        RESULT = False

    except Exception as e:
        RESULT = False
        logger.info(e)
        logger.info('Achat non-effectué')
        driver.save_screenshot('capture_error_'+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.png')
        logger.info("ERROR Detecter, screenshot ok")


    driver.close();
    driver.quit();
    driver = None;
    return RESULT
