import util

def card_is_ok(link):
    tree = util.get_tree(link)
    dispo = tree.xpath(f"//div[@class='website']//span[1]/text()")[0]
    dispo_p2 = tree.xpath(f"//em[normalize-space()='stock']/text()")
    if len(dispo_p2) >= 1 :
        dispo = dispo + dispo_p2[0]

    if not 'En stock' == dispo:
        return False

    prix_ = tree.xpath(f"//body/div[@class='main product-detail']/div[@id='activeOffer']/div[@class='product-info']/div[@class='wrap-aside']/aside/div[@class='price']/div[1]/text()")[0]
    prix = util.make_num(prix_)
    title =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h1[1]/text()")[0].strip()
    desc =  tree.xpath(f"/html[1]/body[1]/div[3]/div[2]/div[1]/h2[1]/text()")[0].strip()

    if 'StarTech.com' in title and 'thermique' in title and prix == 5:  # For test https://www.ldlc.com/fiche/PB00240495.html
        return True

    if not 'LHR'.lower() in desc.lower() and not 'LHR'.lower() in title.lower():
        if 'HDMI/Tri DisplayPort'.lower() in desc.lower():

            if '3080' in title.lower():
                if 710 <= prix <= 730:
                    return True

            elif '3060' in title.lower() and 'TI'.lower() in title.lower():
                if 410 <= prix <= 430:
                    return True

            elif '3070' in title.lower():
                if 510 <= prix <= 530:
                    return True

            elif '3090' in title.lower():
                if 1540 <= prix <= 1560:
                    return True

    return False
