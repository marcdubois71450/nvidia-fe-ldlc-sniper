import util

def card_is_ok(link, logger):
    logger.info('Check if card is ok | {}'.format(link))
    tree = util.get_tree(link)
    dispo = tree.xpath(f"//div[@class='website']//span[1]/text()")[0]
    dispo_p2 = tree.xpath(f"//em[normalize-space()='stock']/text()")
    if len(dispo_p2) >= 1 :
        dispo = dispo + dispo_p2[0]

    logger.info('Dispo : {}'.format(dispo))
    if not 'En stock' == dispo:
        return False

    prix_ = tree.xpath(f"//body/div[@class='main product-detail']/div[@id='activeOffer']/div[@class='product-info']/div[@class='wrap-aside']/aside/div[@class='price']/div[1]/text()")[0]
    prix = util.make_num(prix_)
    title =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h1[1]/text()")[0].strip()
    desc =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h2[1]/text()")[0].strip()
    logger.info('Price : {}e'.format(str(prix)))
    logger.info('Titre : {}'.format(title))
    logger.info('Description : {}'.format(desc))

    if 'StarTech.com' in title and 'thermique' in title and prix == 5:  # For test https://www.ldlc.com/fiche/PB00240495.html
        logger.info('Test mode: pate thermique detecter')
        return True

    if not 'LHR'.lower() in desc.lower() and not 'LHR'.lower() in title.lower():
        logger.info('No LHR in title and description')
        if 'HDMI/Tri DisplayPort'.lower() in desc.lower():
            logger.info('Carte Graphique detect')
            if '3080' in title.lower():
                logger.info('3080 Detect')
                if 710 <= prix <= 730:
                    logger.info('Price is ok')
                    return True

            elif '3060' in title.lower() and 'TI'.lower() in title.lower():
                logger.info('3060Ti Detect')
                if 410 <= prix <= 430:
                    logger.info('Price is ok')
                    return True

            elif '3070' in title.lower():
                logger.info('3070 Detect')
                if 510 <= prix <= 530:
                    logger.info('Price is ok')
                    return True

            elif '3090' in title.lower():
                logger.info('3090 Detect')
                if 1540 <= prix <= 1560:
                    logger.info('Price is ok')
                    return True
            else:
                logger.info('No interesting card detect')

        else:
            logger.info('It is not a graphics card.')
    else:
        logger.info('LHR Detect')

    return False
