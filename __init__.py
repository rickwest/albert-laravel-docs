# -*- coding: utf-8 -*-

"""Search the Laravel Documentation"""

from os import path
import urllib.parse
import html
from algoliasearch.search_client import SearchClient

from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Laravel Docs"
__version__ = "0.1"
__trigger__ = "ld "
__author__ = "Rick West"
__dependencies__ = ["algoliasearch"]


client = SearchClient.create("8BB87I11DE", "8e1d446d61fce359f69cd7c8b86a50de")
index = client.init_index("docs")


icon = "{}/icon.png".format(path.dirname(__file__))
google_icon = "{}/google.png".format(path.dirname(__file__))

docs = "https://laravel.com/docs/"


def getSubtitle(hit):
    if hit["h4"] is not None:
        return hit["h4"]

    if hit["h3"] is not None:
        return hit["h3"]

    if hit["h2"] is not None:
        return hit["h2"]

    return None


def handleQuery(query):
    items = []

    if query.isTriggered:

        if not query.isValid:
            return

        if query.string.strip():
            search = index.search(query.string, {"tagFilters": "master"})

            urls = []

            for hit in search["hits"]:
                url = "{}{}".format(docs, hit["link"])

                if url in urls:
                    continue

                urls.append(url)

                title = hit["h1"]
                subtitle = getSubtitle(hit)

                text = False
                try:
                    text = hit["_highlightResult"]["content"]["value"]
                except KeyError:
                    pass

                if text and subtitle:
                    title = "{} - {}".format(title, subtitle)
                    subtitle = text

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text=html.unescape(title),
                        subtext=html.unescape(subtitle),
                        actions=[UrlAction("Open in the Laravel Documentation", url)],
                    )
                )

            if len(items) == 0:
                term = "laravel {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=google_icon,
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[UrlAction("No match found. Search Google", google)],
                    )
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text="Open Docs",
                        subtext="No match found. Open laravel.com/docs...",
                        actions=[UrlAction("Open the Laravel Documentation", docs)],
                    )
                )

        else:
            items.append(
                Item(
                    id=__prettyname__,
                    icon=icon,
                    text="Open Docs",
                    subtext="Open laravel.com/docs...",
                    actions=[UrlAction("Open the Laravel Documentation", docs)],
                )
            )

    return items
