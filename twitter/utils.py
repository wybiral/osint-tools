from os import environ
from time import sleep

try:
    from twitter import Api
except:
    print('Requires python-twitter: pip install python-twitter')
    exit(1)


class Twitter:

    def __init__(self, **kwargs):
        # Instantiate Twitter API
        # Set env variables with values from https://developer.twitter.com/apps
        self.api = Api(
            consumer_key=environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=environ['TWITTER_CONSUMER_SECRET'],
            access_token_key=environ['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=environ['TWITTER_ACCESS_TOKEN_SECRET'],
        )

    def stream_sample(self):
        # backoff to avoid being put in timeout by Twitter if errors occur
        backoff = 1
        while True:
            try:
                for tweet in self.api.GetStreamSample():
                    # Reset backoff since request succeeded
                    backoff = 1
                    yield tweet
            except Exception as e:
                # Sometimes GetStreamSample connection fails
                sleep(backoff)
                # exponential backoff for repeated errors
                backoff *= 2
