#! /usr/bin/env python3

import newspaper
from newspaper import Article

def main():
    uri = 'http://www.foxbusiness.com/politics/2017/04/11/health-care-reform-first-will-pave-way-for-tax-reform-trump-exclusive.html'

    article = Article(uri)

    article.download()
    article.parse()

    print(article.authors)
    print(article.text)

if __name__ == '__main__':
    main()
