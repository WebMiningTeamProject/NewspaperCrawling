class NewsArticle:

    def __init__(self, news_provider=None, source_uri=None, author=None, title=None, text=None):
        self.news_provider = news_provider
        # Suggested for PK as it should be identifying the article uniquely
        self.source_uri = source_uri
        self.title = title
        self.text = text
        self.author = author

    def __str__(self):
        return 'Provider: %s , Author: %s, Source_URI: %s, Text: %s' \
                % (self.news_provider.name, self.author, self.source_uri, self.text)

    def __hash__(self):
        return self.source_uri

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class NewsProvider:

    def __init__(self, name, rss_uri):
        # Could also be PK
        self.name = name
        self.rss_uri = rss_uri

    def __hash__(self):
        return self.name

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

"""
CREATE TABLE `NewsProvider` (
 `name` VARCHAR(255) NOT NULL,
  `rss_uri` varchar(511) NOT NULL,
 PRIMARY KEY (`name`)
);


CREATE TABLE `NewsArticles` (
 `source_uri` varchar(511) NOT NULL,
 `news_provider` VARCHAR(255),
 `text` TEXT DEFAULT NULL,
 `title` varchar(300) DEFAULT NULL,
 `author` varchar(300) DEFAULT NULL,
 `added_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
 PRIMARY KEY (`source_uri`),
FOREIGN KEY (`news_provider`) REFERENCES `NewsProvider` (`name`) ON DELETE SET NULL ON UPDATE NO ACTION
);
"""
