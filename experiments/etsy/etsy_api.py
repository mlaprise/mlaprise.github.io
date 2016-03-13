import urllib
import requests


class Etsy(object):
    '''Minimalist wrapper around Etsy API.'''

    def __init__(self, etsy_apikey, etsy_secret):
        self.base_url = 'https://openapi.etsy.com/v2'
        self.apikey = etsy_apikey
        self.secret = etsy_secret


    def get_listing(self):
        '''Get the most recent active listings on Etsy.

        :return: The raw JSON response.
        '''
        endpoint= '/listings/active'
        req_url = '{}{}?api_key={}'.format(self.base_url, endpoint, self.apikey)
        return requests.get(req_url).json()


    def get_shop_listing(self, shop_id, page=1, limit=100, fields=['title', 'description']):
        '''Get the listing of a specific shop.

        :param shop_id: Unique id of of the shop.
        :param page: Pagination.
        :param limit: Number of items per page.
        :param fields: Fields to include in the result.
        :return: The raw JSON response.
        '''
        endpoint = '/shops/{}/listings/active'.format(shop_id)
        args = {'page': page,
                'limit': limit}

        if fields != 'all':
            args['fields'] = ','.join(fields)

        req_url = '{}{}?api_key={}&{}'.format(self.base_url, endpoint, self.apikey, urllib.urlencode(args))
        return requests.get(req_url).json()
