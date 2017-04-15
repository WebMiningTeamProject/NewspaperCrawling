
from model import NewsArticle, NewsProvider
from feedparser import parse
from pprint import pprint


def get_articles(news_provider):
    entries = parse(news_provider.rss_uri)['entries']
    return [NewsArticle()
            for e in entries]



def test():
    CNN = NewsProvider('CNN_US', 'http://rss.cnn.com/rss/edition_us.rss')
    feed = get_articles(CNN)
    pprint(feed)


if __name__ == '__main__':
    test()
