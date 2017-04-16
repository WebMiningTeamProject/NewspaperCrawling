# NewspaperCrawling
Crawling Articles from Newspapers

## needed
+ get_rss_providers method from DatbaseHandler class

## Process
0. enter list of RSS sources in DB
0. Crawl RSS feeds of given resources
0. persist a <uri (PK), title, source> tuple in DB
0. [do a prefiltering]
0. crawl URIs and fetch articles
0. extract articles
0. persist article body in DB

*do it all somehow paralell*

# Guidelines
+ Project interpreter will be python3
+ try to maintain PEP8 style convention
+ make sure your ide uses the .editorconfig

# Requirements
install with `pip3 -r requirements.txt`

## Package Newspaper:
Git: https://github.com/codelucas/newspaper 
Walkthrough: Newspaper Crawling.ipynb  (Jupyter/iPython Notebook)
Adding a new source: https://github.com/codelucas/newspaper/blob/master/docs/user_guide/advanced.rst
