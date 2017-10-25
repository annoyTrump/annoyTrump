"""
This app is meant to run continuously in the background. It is written using Python 3.6 and Pycharm.

For this script to work, a user must go to Twitter.com, log in and following the below steps:
    * Navigate your browser to apps.twitter.com
    * Click the 'Create New App' button
    * Fill out the details and agree to the developer agreement.
    * Go to the Keys and Access Tokens tab.
    * Copy the Consumer Key and Consumer Secret into the constants below.
    * At the bottom of the browser window, create access tokens. Copy the Access token and Access Token Secret into 
    the constants below too.
    * Run the script in your favorite IDE or from the command line with ```python -m annoy_trump.main``` You'll need 
    the dependent library TwitterAPI in order to run it. Install TwitterAPI with the command ```pip install TwitterAPI```
"""

from TwitterAPI import TwitterAPI
from time import time, sleep, strptime, ctime
from random import randint
from collections import deque
import json


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''

DELETE_TWITTER_LINKS = [
    'https://support.twitter.com/articles/15358',
    'https://www.pcmag.com/article2/0,2817,2479908,00.asp',
    'https://www.howtogeek.com/280483/how-to-delete-your-twitter-account/',
    'https://www.youtube.com/watch?v=lWIFAX8oC24',
    'https://www.imore.com/how-delete-your-twitter-account',
    'http://www.wikihow.com/Delete-a-Twitter-Account',
    'https://www.purevpn.com/blog/how-to-delete-twitter-account/',
    'https://www.youtube.com/watch?v=AXHZaDiBKsU'
]

MESSAGE = (
    '@realDonaldTrump, {action}! You\'re {noun}. #ImpeachTrump '
    '{link}'
)

# Twitter will reject 'repeat' tweets so we have to mix it up with different messages.
NOUNS = [
    'an embarrassment',
    'a loser',
    'pathetic',
    'reckless',
    'tactless',
    'villainous',
    'a lame duck',
    'a hypocrite',
    'a mistake',
]

ACTIONS = [
    'delete your twitter',
    'put down the phone',
    'drop the golf clubs',
    'do your job',
    'help Puerto Rico 🇵🇷'
]


def main():
    """
    Sends Donald Trump, the saddest excuse of a President the United States has seen, a tweet urging him to delete 
    his account. And because he might not know how to do that, we'll even provide him a link.
    
    :return: None
    """
    i = 0
    recent_messages = deque(maxlen=3)
    retry_post = None
    while True:
        time_now = time()
        time_now_hr = strptime(ctime(time_now), '%a %b %d %H:%M:%S %Y',)
        
        # Every morning at 8 am, try to spread how people can join the Revolution against Trump.
        if time_now_hr.tm_min == 0 and time_now_hr.tm_sec <= 10 and time_now_hr.tm_hour == 8:
            try:
                api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
                request = api.request(
                    'statuses/update',
                    {
                        'status': 'Want to tell @realDonaldTrump how bad he is doing every hour? '
                                  'Download this Python script. https://github.com/annoyTrump/annoyTrump'
                    }
                )
                if request.status_code == 200:
                    print('\033[92m' + '\r\nSent ad.' + '\033[0m')
                else:
                    print('Ad could not be sent.')
            except (TimeoutError, TwitterConnectionError):
                pass
            
        # Every hour, tweet at 45, calling him out on his lack of leadership and overuse of Twitter and golfing.
        if time_now % 3600 < 10 or (retry_post is not None and retry_post is True):
            retry_post = False
            try:
                link = randint(0, len(DELETE_TWITTER_LINKS) - 1)
                noun = randint(0, len(NOUNS) - 1)
                action = randint(0, len(ACTIONS) - 1)
                message = MESSAGE.format(link=DELETE_TWITTER_LINKS[link], noun=NOUNS[noun], action=ACTIONS[action])
                while message in recent_messages:
                    link = randint(0, len(DELETE_TWITTER_LINKS) - 1)
                    noun = randint(0, len(NOUNS) - 1)
                    action = randint(0, len(ACTIONS) - 1)
                    message = MESSAGE.format(link=DELETE_TWITTER_LINKS[link], noun=NOUNS[noun], action=ACTIONS[action])
                recent_messages.append(message)

                # tell Trump how to delete his account
                api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
                request = api.request(
                    'statuses/update',
                    {
                        'status': message
                    }
                )
                if request.status_code == 200:
                    print('\033[92m' + '\r\nSent {msg}.'.format(msg=message) + '\033[0m')
                else:
                    errors = json.loads(request.text)['errors']
                    # if Twitter says this is a duplicate, then increase the maxlen of the deque
                    if len(errors) == 1 and errors[0]['code'] == 187:
                        # create a new deque with the old deque items in it. Increase maxlen by one.
                        recent_messages = deque(recent_messages, maxlen=recent_messages.maxlen + 1)
                        # append the most recent message that was denied.
                        recent_messages.append(message)
                        print('\r\nPost was denied. Trying to post another one.')
                        retry_post = True
                    else:
                        print('\r\nError ' + request.status_code + '. ' + request.text + ': ' + message)
                sleep(60)
            except (TimeoutError, TwitterConnectionError):
                pass
        else:
            if i == 0:
                print('\r\nsleeping')
                i = 255
            else:
                print(['z', 'Z', ' '][randint(0, 2)], end='', flush=True)
                i -= 1
            sleep(10)

if __name__ == '__main__':
    main()
