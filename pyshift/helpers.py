# coding: utf-8

import os
import yaml
import time
import hashlib

BASE_DIR = os.path.dirname(__file__)

SETTINGS = os.path.join(BASE_DIR, 'settings.yml')


def load_settings():
    with open(SETTINGS) as f:
        settings = yaml.load(f)
    return settings


def make_transation_id():
    order_id = str.encode(str(int(time.time())))
    hash_order_id = hashlib.md5(order_id).hexdigest()

    return hash_order_id
