import nltk

from collections import defaultdict
from operator import itemgetter
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from etsy_api import Etsy

EN_STOPWORDS = set(nltk.corpus.stopwords.words())
EN_STOPWORDS = EN_STOPWORDS.union(set(['etsy', 'www', 'http', 'https', 'shop']))

ETSY_APIKEY = 'defmtlk9o2c64r3587c08qza'
ETSY_SECRET = 'i5xax0ccnn'

toker = RegexpTokenizer(r'\w{3,}')


def items_listing_generator(shop_id):
    '''Fetch all items title and description for a specific etsy shop.

    :param shop_id: Etsy shop id.
    '''
    page = 1
    while page:
        response = etsy_api.get_shop_listing(shop_id, page=page)
        page = response['pagination']['next_page']
        for item in response['results']:
            yield u"{} {}".format(item['title'], item['description'])


def unigram_generator(docs):
    '''Iterate through a list of document and yield token.

    :param docs: A list of documents string.
    '''
    for full_content in docs:
        for sent in nltk.sent_tokenize(full_content):
            tokenized_content =  [t.lower() for t in toker.tokenize(sent) if t.lower() not in EN_STOPWORDS]
            for tok in tokenized_content:
                yield tok


def get_top_terms(shop_items, top_n = 5):
    '''Get the top terms (unigram) for a Etsy shop.

    :param shop_items: List of all the shop items.
    :param top_n: Return the top_n terms.
    :return: List of top terms. Each item is a tuple (term, frequency)
    '''
    terms_freq = defaultdict(int)
    for unigram in unigram_generator(shop_items):
        terms_freq[unigram] += 1
    top_terms = sorted(terms_freq.items(), key=itemgetter(1), reverse=True)[:5]
    return top_terms


if __name__ == "__main__":
    etsy_shops = ['laplumeblanche',
                  'LesNanaseries',
                  'HoneyCanada',
                  'ParasolsbyDesign',
                  'ShinySteelDrums',
                  'CakeInTheMorn',
                  'PicasoLab',
                  'bertiescloset',
                  'TheComposersPen',
                  'SupremerStudio']

    etsy_api = Etsy(ETSY_APIKEY, ETSY_APIKEY)

    for shop_id in etsy_shops:
        print "\nEtsy Shop: {}".format(shop_id)
        shop_items = items_listing_generator(shop_id)
        print get_top_terms(shop_items)
