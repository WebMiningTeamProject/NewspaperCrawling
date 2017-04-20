#! /usr/bin/env python3

import os
import sys
import logging
import configparser
import argparse
import crawler
from DatabaseHandler import DatabaseHandler
from model import *

LOGGER = logging.getLogger()


def parse_args():
    """
    initiates the argparseres and returns configpath gotten from parser
    """
    parser = argparse.ArgumentParser(
        description='Crawls newspages', prog='crawler')

    parser.add_argument(
        '-c',
        type=str,
        nargs='?',
        dest='config',
        required=True,
        help='path to configfile')
    args = parser.parse_args()
    return args.config


def load_config(config_file):
    """
    Loads config from config file and returns it
    """
    cparser = configparser.ConfigParser()
    try:
        cparser.read(config_file)
        return cparser
    except Exception as exc:
        print(exc)
        sys.exit(1)


def init_logging(log_path):
    """
    This will initiate the logging by setting the loglevel and creating the logfile.
    """
    LOGGER.setLevel(logging.WARNING)
    try:
        file_log_handler = logging.FileHandler(log_path)
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    file_log_handler.setFormatter(formatter)
    LOGGER.addHandler(file_log_handler)


def feedparse():
    import feedparser
    CNN = NewsProvider('CNN_US', 'http://rss.cnn.com/rss/edition_us.rss')

    feed = feedparser.parse(CNN.rss_uri)
    entry = feed.get('entries')
    l = entry[0].get('link')
    print(entry)
    print(l)


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    config_file = parse_args()
    conf = load_config(config_file)
    init_logging(conf['DEFAULT']['LogPath'])


    dh = DatabaseHandler(
        host=conf['DATABASE']['Host'],
        user=conf['DATABASE']['User'],
        password=conf['DATABASE']['Password'],
        db_name=conf['DATABASE']['DB']
    )

    #CNN = NewsProvider('CNN_US', 'http://rss.cnn.com/rss/edition_us.rss')
    #dh.persistNewsProviders([CNN])

    np = dh.readNewsProvider()

    crawler.get_articles_from_news_providers(np, dh)

    dh.close()

if __name__ == '__main__':
    main()
