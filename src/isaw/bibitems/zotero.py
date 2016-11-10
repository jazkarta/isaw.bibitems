import requests
from bs4 import BeautifulSoup
from five import grok
from json import loads
from pyzotero import zotero
from urlparse import urlparse
from . import logger
from .interfaces import IBibliographicURLIFetcher


class ZoteroWebParser(grok.GlobalUtility):
    grok.implements(IBibliographicURLIFetcher)
    grok.name('www.zotero.org')

    library_id = None
    library_type = None
    item_id = None

    def fetch(self, uri):
        url_path = urlparse(uri).path
        path_parts = url_path.split('/')
        if 'itemKey' in path_parts:
            self.item_id = path_parts[path_parts.index('itemKey') + 1]
        else:
            # Guess?
            self.item_id = path_parts[-1]

        try:
            response = requests.get(uri)
        except requests.exceptions.RequestException:
            logger.exception('Error fetching Zotero web page.')
            return {u"error": u"Could not fetch web page"}

        if response.status_code >= 400:
            return {u"error": u"Could not fetch web page"}

        parsed = BeautifulSoup(response.text, "lxml")
        details = parsed.find(id=u"item-details-div")
        if not details:
            return {u"error": u"Could not find item-details-div"}

        info = loads(details.get('data-loadconfig', '{}'))
        self.library_id = info.get('libraryID')
        self.library_type = info.get('libraryType')

        if not self.library_id:
            return {u"error": u"Could not find determine library id"}

        if not self.library_type:
            return {u"error": u"Could not find determine library id"}

        data = self._zotero_api_result()
        result = {}
        if data.get('data'):
            info = data['data']
            result[u'short_title'] = info['shortTitle']
            result[u'title'] = info['title']
            result[u'formatted_citation'] = data['formatted']
            result[u'access_uri'] = info['url']
            result[u'bibliographic_uri'] = data['links']['alternate']['href']
            authors = result[u'authors'] = []
            editors = result[u'editors'] = []
            contributors = result[u'contributors'] = []
            for item in info.get('creators', []):
                if item['creatorType'] == 'author':
                    authors.append("{}, {}".format(item['lastName'],
                                                   item['firstName']))
                if item['creatorType'] == 'editor':
                    editors.append("{}, {}".format(item['lastName'],
                                                   item['firstName']))
                if item['creatorType'] == 'contributor':
                    contributors.append("{}, {}".format(item['lastName'],
                                                        item['firstName']))
            result[u'publisher'] = info.get(u'publisher')
            result[u'isbn'] = info.get(u'ISBN')
            result[u'issn'] = info.get(u'ISSN')
            result[u'doi'] = info.get(u'DOI')
            result[u'date_of_publication'] = info.get(u'date')
            result[u'text'] = info.get('abstractNote')
            result[u'parent_title'] = (
                info.get('blogTitle') or info.get('bookTitme') or
                info.get('dictionaryTitle') or info.get('encyclopediaTitle') or
                info.get('forumTitle') or info.get('proceedingsTitle') or
                info.get('publicationTitle') or info.get('websiteTitle')
            )
            result[u'volume'] = info.get('volume')
            result[u'range'] = info.get('pages')

        if isinstance(result.get(u'formatted_citation'), list):
            result[u'formatted_citation'] = result[u'formatted_citation'][0]

        return result

    def _zotero_api_result(self):
        api = zotero.Zotero(self.library_id, self.library_type)
        results = api.item(self.item_id, format='json')
        formatted = api.item(self.item_id, content='bib')
        results['formatted'] = formatted

        return results
