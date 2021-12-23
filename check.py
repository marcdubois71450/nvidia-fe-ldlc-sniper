import util

def card_is_ok(link):
    print('Check if card is ok | {}'.format(link))
    tree = util.get_tree(link)
    dispo = tree.xpath(f"//div[@class='website']//span[1]/text()")[0]
    dispo_p2 = tree.xpath(f"//em[normalize-space()='stock']/text()")
    if len(dispo_p2) >= 1 :
        dispo = dispo + dispo_p2[0]

    print('Dispo : {}'.format(dispo))
    if not 'En stock' == dispo:
        return False

    prix_ = tree.xpath(f"//body/div[@class='main product-detail']/div[@id='activeOffer']/div[@class='product-info']/div[@class='wrap-aside']/aside/div[@class='price']/div[1]/text()")[0]
    prix = util.make_num(prix_)
    title =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h1[1]/text()")[0].strip()
    desc =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h2[1]/text()")[0].strip()
    print('Price : {}e'.format(str(prix)))
    print('Titre : {}'.format(title))
    print('Description : {}'.format(desc))

    if 'StarTech.com' in title and 'thermique' in title and prix == 5:  # For test https://www.ldlc.com/fiche/PB00240495.html
        print('Test mode: pate thermique detecter')
        return True

    if not 'LHR'.lower() in desc.lower() and not 'LHR'.lower() in title.lower():
        print('No LHR in title and description')
        if 'HDMI/Tri DisplayPort'.lower() in desc.lower():
            print('Carte Graphique detect')
            if '3080' in title.lower():
                print('3080 Detect')
                if 710 <= prix <= 730:
                    print('Price is ok')
                    return True

            elif '3060' in title.lower() and 'TI'.lower() in title.lower():
                print('3060Ti Detect')
                if 410 <= prix <= 430:
                    print('Price is ok')
                    return True

            elif '3070' in title.lower():
                print('3070 Detect')
                if 510 <= prix <= 530:
                    print('Price is ok')
                    return True

            elif '3090' in title.lower():
                print('3090 Detect')
                if 1540 <= prix <= 1560:
                    print('Price is ok')
                    return True
            else:
                print('No interesting card detect')

        else:
            print('It is not a graphics card.')
    else:
        print('LHR Detect')

    return False
