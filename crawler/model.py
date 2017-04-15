class NewsArticle:

    def __init__(self, news_provider=None, source_uri=None, author=None, text=None):
        self.news_provider = news_provider
        self.source_uri = source_uri
        self.text = text
        self.author = author

    def __str__(self):
        return 'Provider: %s , Author: %s, Source_URI: %s, Text: %s' \
                % (self.news_provider.name, self.author, self.source_uri, self.text)

class NewsProvider:

    def __init__(self, name, rss_uri):
        self.name = name
        self.rss_uri = rss_uri
