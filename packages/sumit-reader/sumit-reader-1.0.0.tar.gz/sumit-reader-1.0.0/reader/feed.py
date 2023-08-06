import feedparser
import html2text
_CACHED_FEEDS = dict()

def _feed(url):
    if url not in _CACHED_FEEDS:
        _CACHED_FEEDS[url] = feedparser.parse(url)
        return _CACHED_FEEDS[url]