import tweepy

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

        print('New tweet')

        links = []
        for link in status._json['entities']['urls']:
            links.append(str(link['expanded_url']))

        if len(links) == 0:
            print('No link in this tweet')
        else:
            for link in links:
                if 'ldlc.com' in link:
                    if card_is_ok(link):
                        buy_ldlc(link, LDLC_ACCOUNT, CARD)
                    else:
                        print('Card nok | {}'.format(link))
                else:
                    print('Link no ldlc | {}'.format(link))

if __name__ == "__main__":
    printer = IDPrinter(
      consumer_key, consumer_secret,
      access_token, access_token_secret
    )
    print('Start listening twitter notification')
    printer.filter(follow=['3068657781', '1183649809871310848', '1401296037147549697'])
                            # marc            bavarnold           dropreference
