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
        trs = table.find_all('tr')
        # Skip header row
        trs = trs[1:]
        for tr in trs:
            tds = tr.find_all('td')
            a = tds[0].find('a')
            paste_id = a['href'][1:]
            if paste_id in cache:
                # Ignore recently seen
                continue
            obj = {'id': paste_id, 'title': a.string}
            syntax = tds[2].string
            if syntax != '-':
                # Check for syntax
                obj['syntax'] = syntax
            yield obj
            cache.append(paste_id)
            if len(cache) > MAX_CACHE:
                cache = cache[-MAX_CACHE:]
        sleep(CRAWL_DELAY)

# Start at main if executed as a program
if __name__ == '__main__':
    main()
