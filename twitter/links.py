from json import dumps
from os import environ
from time import sleep

try:
    from twitter import Api
except:
    print('Requires python-twitter: pip install python-twitter')
    exit(1)

# Instantiate Twitter API
# Set env variables with values from https://developer.twitter.com/apps
api = Api(
    consumer_key=environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=environ['TWITTER_ACCESS_TOKEN_SECRET'],
)

# Read tweet objects and write to stdout as newline-delimited JSON
def main():
    for tweet in twitter_stream():
        print(dumps(tweet), flush=True)

# Infinitely stream URL origins from Twitter links in real-time
def twitter_stream():
    # backoff to avoid being put in timeout by Twitter if errors occur
    backoff = 1
    while True:
        try:
            for tweet in api.GetStreamSample():
                # Reset backoff since request succeeded
                backoff = 1
                if 'entities' not in tweet:
                    continue
                entities = tweet['entities']
                if 'urls' not in entities:
                    continue
                links = set()
                for url in entities['urls']:
                    if 'unwound' in url:
                        u = url['unwound']['url']
                    else:
                        u = url['expanded_url']
                    # Ignore tweet links
                    if u.startswith('https://twitter.com'):
                        continue
                    links.add(u)
                if not links:
                    continue
                yield {
                    'tweet_id': tweet['id_str'],
                    'user_id': tweet['user']['id_str'],
                    'links': sorted(links),
                }
        except Exception as e:
            # Sometimes GetStreamSample connection fails
            sleep(backoff)
            # exponential backoff for repeated errors
            backoff *= 2


# Start at main if executed at a program
if __name__ == '__main__':
    main()
