'''
Stream newline-delimited JSON of objects of Tweets containing links.

Structure:
{"tweet_id": <str>, "user_id": <str>, "links": [list of url strings]}

Data obtained from real-time Twitter API stream sample.
'''

from json import dumps
from utils import Twitter

def main():
    try:
        for tweet in twitter_links():
            print(dumps(tweet), flush=True)
    except KeyboardInterrupt:
        return

# Yields tweets with links from Twitter stream sample.
# Each yielded objects contains tweet_id, user_id, links[]
def twitter_links(**kwargs):
    twitter = Twitter(**kwargs)
    for tweet in twitter.stream_sample():
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

# Start at main if executed as a program
if __name__ == '__main__':
    main()
