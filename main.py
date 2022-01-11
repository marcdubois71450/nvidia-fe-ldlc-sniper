import time
import tweepy
import logging
from logging.handlers import SysLogHandler

from check import card_is_ok
from buy import buy_ldlc

from config import LDLC_ACCOUNT, CARD, consumer_key, consumer_secret, access_token, access_token_secret, list_account

class NvidiaTweetStream(tweepy.Stream):
    def on_connect(self):
        logger.info('Twitter API | Connected')
        return

    def on_disconnect_message(self, notice):
        logger.info('Twitter API | Disconnected: {}'.format(str(notice.code)))
        return

    def on_limit(self, track):
        logger.info('Twitter API | Receive limit has occurred: {}'.format(str(track)))
        return

    def on_warning(self, notice):
        logger.info('Twitter API | Warning message: {}'.format(str(notice.message)))
        return

    def on_exception(self, exception):
        logger.info('Twitter API | Exception error: {}'.format(str(exception)))
        return

    def on_request_error(self, status_code):
        logger.info('Twitter API | Error status_code: {} | retry...'.format(str(status_code)))
        return True

    def on_connection_error(self):
        logger.info('Twitter API | Error timeout, retry...')
        return True

    def on_status(self, status):
        user_id = str(status._json['user']['id'])
        if user_id in list_account:
            logger.info('New tweet | https://twitter.com/twitter/statuses/{}'.format(str(status._json['id'])))
            links = []
            for link in status._json['entities']['urls']:
                links.append(str(link['expanded_url']))

            if len(links) == 0:
                logger.info('No link in this tweet')
            else:
                for link in links:
                    if 'https://www.ldlc.com/' in link:
                        link = link.split('?')[0]
                        logger.info('New ldlc link | {}'.format(link))

                        if 'es-es/ficha' in link:
                            link = link.replace('es-es/ficha', 'fiche')

                        if 'it-it/scheda' in link:
                            link = link.replace('it-it/scheda', 'fiche')


                        if len(LINK_TESTED) >= 100:
                            LINK_TESTED.pop(0)


                        if not link in LINK_TESTED:

                            card_status = card_is_ok(link, logger)

                            LINK_TESTED.append(link)

                            if card_status == 'retry':
                                logger.info('Retry Check | {}'.format(link))
                                retry = 0
                                while True:
                                    time.sleep(0.75)
                                    retry = retry + 1
                                    card_status_new = card_is_ok(link, logger)

                                    if card_status_new == 'retry' and retry < 30:
                                        logger.info('Retry Check | {}'.format(link))
                                        continue

                                    card_status = card_status_new
                                    break

                            card_status = card_status_new

                            if card_status == 'no':
                                logger.info('Card nok | {}'.format(link))
                            elif card_status == 'yes':
                                r = buy_ldlc(link, LDLC_ACCOUNT, CARD, logger)
                                if r:
                                    logger.info('Order Success | {}'.format(link))
                                else:
                                    logger.info('Order Fail | {}'.format(link))
                            else:
                                logger.info('Card nok max retry check | {}'.format(link))
                        else:
                            logger.info('This link is already tested | {}'.format(link))
                    else:
                        logger.info('No Ldlc link | {}'.format(link))

if __name__ == "__main__":
    logger = logging.getLogger("nvidia-fe-ldlc-sniper")
    logger.setLevel('DEBUG')
    syslog = SysLogHandler('/dev/log', 'syslog')
    syslog.setLevel('DEBUG')
    format_str = "nvidia-fe-ldlc-sniper: {message}"
    formatter = logging.Formatter(format_str, style="{")
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.info("nvidia-fe-ldlc-sniper started")


    LINK_TESTED = []

    while True:
        printer = NvidiaTweetStream(
          consumer_key, consumer_secret,
          access_token, access_token_secret
        )
        logger.info('Start listening twitter notification...')
        printer.filter(follow=list_account)
