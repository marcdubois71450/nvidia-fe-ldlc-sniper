import util
import time
from random import randrange

from config import ACTIVATE

def card_is_ok(link, logger):

    if '?' in link.split('/')[-1]:
        link = link + '&timestamp{}={}'.format(str(randrange(0, 9999)), str(time.time()).replace('.', ''))
    else:
        link = link + '?timestamp{}={}'.format(str(randrange(0, 9999)), str(time.time()).replace('.', ''))

    logger.info('Check if card is ok | {}'.format(link))

    try:
        tree = util.get_tree(link)
        dispo = tree.xpath(f"//div[@class='website']//span[1]/text()")[0]
        dispo_p2 = tree.xpath(f"//em[normalize-space()='stock']/text()")
        if len(dispo_p2) >= 1 :
            dispo = dispo + dispo_p2[0]

    except Exception as e:
        logger.info(e)
        logger.info('Fail parse data ldlc retry')
        return 'retry'


    logger.info('Dispo : {}'.format(dispo))
    if not 'En stock' == dispo:
        logger.info('Non En Stock retry')
        return 'retry'

    try:
        prix_ = tree.xpath(f"//body/div[@class='main product-detail']/div[@id='activeOffer']/div[@class='product-info']/div[@class='wrap-aside']/aside/div[@class='price']/div[1]/text()")[0]
        prix = util.make_num(prix_)
        title = tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h1[1]/text()")[0].strip()
        desc = tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h2[1]/text()")[0].strip()
        logger.info('Price : {}e'.format(str(prix)))
        logger.info('Titre : {}'.format(title))
        logger.info('Description : {}'.format(desc))
    except Exception as e:
        logger.info(e)
        logger.info('Fail parse data ldlc etry')
        return 'retry'


    if 'https://www.ldlc.com/fiche/PB00102559.html'.lower() in link.lower():  # For test https://www.ldlc.com/fiche/PB00102559.html
        logger.info('Test mode: bic bleu detecter')
        return 'yes'

    if not 'LHR'.lower() in desc.lower() and not 'LHR'.lower() in title.lower():
        if 'HDMI/Tri DisplayPort'.lower() in desc.lower():
            if '3080' in title.lower():
                logger.info('3080 Detect')
                if 710 <= prix <= 730:
                    logger.info('Price is ok')
                    if ACTIVATE['3080']:
                        return 'yes'
                    else:
                        logger.info('3080 is not activated')
                        return 'no'

                if '12 Go GDDR6' in desc.lower():
                    if 710 <= prix <= 1100:
                        logger.info('Price is ok')
                        if ACTIVATE['3080']:
                            return 'yes'
                        else:
                            logger.info('3080 is not activated')
                            return 'no'

            elif '3060' in title.lower() and 'TI'.lower() in title.lower():
                logger.info('3060Ti Detect')
                if 410 <= prix <= 430:
                    logger.info('Price is ok')
                    if ACTIVATE['3060']:
                        return 'yes'
                    else:
                        logger.info('3060 is not activated')
                        return 'no'

            elif '3070' in title.lower():
                logger.info('3070 Detect')
                if 510 <= prix <= 530:
                    logger.info('Price is ok')
                    if ACTIVATE['3070']:
                        return 'yes'
                    else:
                        logger.info('3070 is not activated')
                        return 'no'

            elif '3090' in title.lower():
                logger.info('3090 Detect')
                if 1540 <= prix <= 1560:
                    logger.info('Price is ok')
                    if ACTIVATE['3090']:
                        return 'yes'
                    else:
                        logger.info('3090 is not activated')
                        return 'no'
            else:
                logger.info('No interesting card detect')

        else:
            logger.info('It is not a graphics card.')
    else:
        logger.info('LHR Detect')

    return 'no'
