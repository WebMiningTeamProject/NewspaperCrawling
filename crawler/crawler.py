#! /usr/bin/env python3

import os
import sys
import logging
import configparser
import argparse
from DatabaseHandler import DatabaseHandler

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
        return cparser.read(config_file)
    except Exception as exc:
        print(exc)
        sys.exit(1)


def init_logging(log_path):
    """
    This will initiate the logging by setting the loglevel and creating the logfile.
    """
    LOGGER.setLevel(logging.INFO)
    try:
        file_log_handler = logging.FileHandler(log_path)
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    file_log_handler.setFormatter(formatter)
    LOGGER.addHandler(file_log_handler)
    LOGGER.addHandler(file_log_handler)


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    config_file = parse_args()
    conf = load_config(config_file)
    init_logging(conf['DEFAULT']['LogPath'])
    dh = DatabaseHandler(
        host=conf['Database']['Host'],
        user=conf['Database']['User'],
        password=conf['Database']['Password'],
        db= conf['Database']['DB']
    )


if __name__ == '__main__':
    main()
