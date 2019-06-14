# pastebin

Scrape recent paste metadata from pastebin in real-time.

Streams newline-delimited JSON to stdout with the keys `id`, `title`, and `syntax` (if there is one).

You can access the paste content using pastebin.com/raw/[id] but they have a habit of temporarily
blocking IP addresses that do this too frequently so use at your own risk (or behind someone else's IP).
