#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Useful utilities for the whole project.
Such as a mongodb client, aconfig getter etc.
"""

from pymongo import MongoClient
import configparser
import os

base_path = os.path.split(os.path.realpath(__file__))[0]
conf_path = base_path + '/config.ini'

def hawkeye_conf():
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config

def get_conf(section, option):
    config = hawkeye_conf()
    return config.get(section=section, option=option)


mongo_cli = MongoClient(host=get_conf('MongoDB', 'HOST'),
                  port=int(get_conf('MongoDB', 'PORT')))
try:
    db = mongo_cli.Hawkeye
    db.authenticate(get_conf('MongoDB', 'ACCOUNT'),
                    get_conf('MongoDB', 'PASSWORD'))
except BaseException:
    db = mongo_cli.Hawkeye

leakage_col = db.leakage
query_col = db.query
blacklist_col = db.blacklist
notice_col = db.notice
