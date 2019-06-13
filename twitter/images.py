'''
Stream newline-delimited JSON of objects of Tweets containing images.

Structure:
{"tweet_id": <str>, "user_id": <str>, "images": [list of url strings]}

Data obtained from real-time Twitter API stream sample.
'''

from json import dumps
from utils import Twitter

def main():
    try:
        for tweet in twitter_images():
            print(dumps(tweet), flush=True)
    except KeyboardInterrupt:
        return

# Yields tweets with images from Twitter stream sample.
# Each yielded objects contains tweet_id, user_id, images[]
def twitter_images(**kwargs):
    twitter = Twitter(**kwargs)
    for tweet in twitter.stream_sample():
        if 'entities' not in tweet:
            continue
        entities = tweet['entities']
        if 'media' not in entities:
            continue
        images = set()
        for media in entities['media']:
            url = media['media_url_https']
            if 'video_thumb' in url:
                # Ignore video thumbnails
                continue
            images.add(url)
        if not images:
            continue
        yield {
            'tweet_id': tweet['id_str'],
            'user_id': tweet['user']['id_str'],
            'images': sorted(images),
        }

# Start at main if executed as a program
if __name__ == '__main__':
    main()
