import tweepy
import logging
from logging.handlers import SysLogHandler



from check import card_is_ok
from buy import buy_ldlc


LDLC_ACCOUNT = {
    'email' : 'user@domain.tld',
    'password': 'amazingpassword'
}

CARD = {
    'num' : 'XXXXXXXXXXXXXXXXXX',
    'date': 'XX/XX',
    'secret': 'XXX',
    'name': 'Xxxxxx Xxxxxxxxxx'
}

# Twitter
consumer_key = 'x'
consumer_secret = 'x'
access_token = 'x'
access_token_secret = 'x'

class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        logger.info('New tweet')

        links = []
        for link in status._json['entities']['urls']:
            links.append(str(link['expanded_url']))

        if len(links) == 0:
            logger.info('No link in this tweet')
        else:
            for link in links:
                if 'ldlc.com' in link:
                    if card_is_ok(link, logger):
                        buy_ldlc(link, LDLC_ACCOUNT, CARD, logger)
                    else:
                        logger.info('Card nok | {}'.format(link))
                else:
                    logger.info('No Ldlc link | {}'.format(link))

if __name__ == "__main__":
    logger = logging.getLogger("nvidia-fe-ldlc-sniper")
    formatter = logging.Formatter('%(asctime)s | %(message)s')
    fileHandler = logging.FileHandler('/var/log/nvidia-sniper.log', mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel('DEBUG')
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


    while True:
        printer = IDPrinter(
          consumer_key, consumer_secret,
          access_token, access_token_secret
        )
        logger.info('Start listening twitter notification...')
        printer.filter(follow=['3068657781', '1183649809871310848', '1401296037147549697'])
                                # marc            bavarnold           dropreference
