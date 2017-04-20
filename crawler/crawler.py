import threading
import queue
from model import NewsArticle, NewsProvider
import feedparser
import itertools
from requests import get
from newspaper import Article as RawArticle



MAX_RSSFETCHER_THREADS = 3
MAX_FETCHER_THREADS = 6
STOP_SIG = threading.Event()



def crawl_rss(news_provider_queue, result_queue):

    while not news_provider_queue.empty():
        news_provider = news_provider_queue.get()
        # get the entries of the rss feed
        entries = feedparser.parse(news_provider.rss_uri)['entries']
        for entry in entries:
            # get the link of each entry and create a news article for it
            uri = entry.get('link')
            news_article = NewsArticle(news_provider=news_provider.name, source_uri=uri)
            # put the article in the queue to let it process by the ArticleFetcher
            result_queue.put(news_article)
        news_provider_queue.task_done()


def crawl_article(article_queue, dh):
    while not (STOP_SIG.is_set() and article_queue.empty()):
        article = article_queue.get()

        raw = RawArticle(article.source_uri)
        raw.download()
        raw.parse()

        article.author = raw.authors
        article.text = raw.text

        dh.persistNewsArticle(article)
        article_queue.task_done()




def get_articles_from_news_providers(news_providers, dh):
    """
    This will fetch the news providers rss feed and fetch the article uri. It will then download the article and persist it
    :param news_providers: array of NewsProviders
    """

    # Build the queues
    news_provider_queue = queue.Queue()
    [news_provider_queue.put(np) for np in news_providers]
    news_article_que = queue.Queue()

    # create threads
    rss_fetchers = [threading.Thread(target=crawl_rss, args=(news_provider_queue, news_article_que))
                    for _ in itertools.repeat(None, MAX_RSSFETCHER_THREADS)]
    article_fetchers = [threading.Thread(target=crawl_article, args=(news_article_que, dh))
                        for _ in itertools.repeat(None, MAX_FETCHER_THREADS)]

    # run threads
    for rss_fetcher in rss_fetchers:
        rss_fetcher.start()


    for article_fetcher in article_fetchers:
        article_fetcher.start()

    # join the rss fetchers
    for thread in rss_fetchers:
        thread.join()
    STOP_SIG.set()

    # join the article_fetchers
    for thread in article_fetchers:
        thread.join()
