# -*- coding: utf-8 -*-

"""Search the Laravel Documentation"""

from os import path
from algoliasearch.search_client import SearchClient

from albertv0 import *

__iid__ = 'PythonInterface/v0.2'
__prettyname__ = 'Laravel Docs'
__version__ = '0.1'
__trigger__ = 'ld '
__author__ = 'Rick West'
__dependencies__ = ['algoliasearch']


client = SearchClient.create('8BB87I11DE', '8e1d446d61fce359f69cd7c8b86a50de')
index = client.init_index('docs')


icon = '{}/icon.png'.format(path.dirname(__file__))


def getSubtitle(hit):
    if hit['h4'] is not None:
        return hit['h4']

    if hit['h3'] is not None:
        return hit['h3']

    if hit['h2'] is not None:
        return hit['h2']

    return ''


def handleQuery(query):
    results = []

    if query.isTriggered and query.string.strip():

        if not query.isValid:
            return

        item = Item(
            id=__prettyname__,
            icon=icon,
            completion=query.rawString,
            text=__prettyname__,
            actions=[]
        )

        if len(query.string) >= 4:
            search = index.search(query, {'tagFilters': 'master'})

            urls = []
            docs = 'https://laravel.com/docs/'

            for hit in search['hits']:
                url = '{}{}'.format(docs, hit['link'])

                if url in urls:
                    continue

                urls.append(url)

                title = hit['h1']
                subtitle = getSubtitle(hit)

                results.append(Item(
                    id=__prettyname__,
                    icon=icon,
                    text=title,
                    subtext=subtitle,
                    actions=[UrlAction('Open in the Laravel Documentation', url)])
                )

            if len(results) == 0:
                item.subtext = 'No results found :('
                return item

        else:
            item.subtext = 'Search the Laravel Documentation!'
            return item
    return results
