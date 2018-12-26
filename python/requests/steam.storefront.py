# -*- coding: utf-8 -*-
import json
import logging
import pprint
import sys

import requests

appId = sys.argv[1]
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def appDetail(appId):
    """
    {
      'name': str,
      'price': {
        'current': Decimal,
        'initial': Decimal,
        'cut': int,
        'currency': str,
      },
      'header_image': str,
    }
    """
    url = 'https://store.steampowered.com/api/appdetails/'
    params = {
        'appids': appId,
        'cc': 'us',
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as err:
        logger.exception('request error')
        return None

    http_code = resp.status_code
    if http_code != 200:
        logger.error('http_code: {}'.format(http_code))
        return None

    result = json.loads(resp.text)
    if str(appId) not in result:
        logger.error('missing appId in result')
        return None

    if not result[str(appId)]['success']:
        logger.error('appId not success')
        return None

    data = result[str(appId)]['data']
    logger.debug(pprint.pformat(data))

    rv = {
        'name': data['name'],
        'header_image': data['header_image'],
        'price': None,
    }
    if not data['release_date']['coming_soon'] and 'price_overview' in data:
        rv['price'] = {
            'cut': data['price_overview']['discount_percent'],
            'currency': data['price_overview']['currency'],
            'current': data['price_overview']['final'],
            'initial': data['price_overview']['initial'],
        },

    return rv


_ = appDetail(appId)
logger.debug(pprint.pformat(_))
