from json import dumps
from time import sleep

try:
    from bs4 import BeautifulSoup
except:
    print('Requires bs4: pip install bs4')
    exit(1)

try:
    import requests
except:
    print('Requires requests: pip install requests')
    exit(1)

# Number of IDs to store in memory to avoid duplicates
MAX_CACHE = 100
# Seconds between crawls
CRAWL_DELAY = 5.0

def main():
    try:
        for paste in paste_stream():
            print(dumps(paste), flush=True)
    except KeyboardInterrupt:
        return

def paste_stream():
    url = 'https://pastebin.com/archive'
    cache = []
    while True:
        r = requests.get(url)
        s = BeautifulSoup(r.content, 'html.parser')
        table = s.find('table', {'class': 'maintable'})
        for a in table.find_all('a'):
            paste_id = a['href'][1:]
            if paste_id.startswith('archive/'):
                # Ignore language archive links
                continue
            if paste_id in cache:
                # Ignore recently seen
                continue
            yield {'id': paste_id, 'title': a.string}
            cache.append(paste_id)
            if len(cache) > MAX_CACHE:
                cache = cache[-MAX_CACHE:]
        sleep(CRAWL_DELAY)

# Start at main if executed as a program
if __name__ == '__main__':
    main()
