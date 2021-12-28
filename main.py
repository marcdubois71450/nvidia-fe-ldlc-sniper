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

class NvidiaTweetStream(tweepy.Stream):
    def on_connect(self):
        logger.info('Twitter API | Connected')
        return

    def on_disconnect_message(self, notice):
        logger.info('Twitter API | Disconnected:' + str(notice.code))
        return

    def on_limit(self, track):
        logger.info('Twitter API | Receive limit has occurred:' + str(track))
        return

    def on_warning(self, notice):
        logger.info('Twitter API | Warning message:' + str(notice.message))
        return

    def on_exception(self, exception):
        logger.info('Twitter API | Exception error:' + str(exception))
        return

    def on_request_error(self, status_code):
        logger.info('Twitter API | Error status_code : {} | retry...'.format(str(status_code)))
        return True

    def on_connection_error(self):
        logger.info('Twitter API | Error timout, retry...')
        return True

    def on_status(self, status):
        logger.info('New tweet | https://twitter.com/twitter/statuses/{}'.format(str(status._json['id'])))
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
    logger.setLevel('DEBUG')
    syslog = SysLogHandler('/dev/log', 'daemon')
    syslog.setLevel('DEBUG')
    format_str = "nvidia-fe-ldlc-sniper: {message}"
    formatter = logging.Formatter(format_str, style="{")
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.info("nvidia-fe-ldlc-sniper started")

    while True:
        printer = NvidiaTweetStream(
          consumer_key, consumer_secret,
          access_token, access_token_secret
        )
        logger.info('Start listening twitter notification...')
        printer.filter(follow=['3068657781', '1183649809871310848', '1401296037147549697'])
                                # marc            bavarnold           dropreference
