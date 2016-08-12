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
        self.item_id = url_path.split('/')[-1]

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
            result['short_title'] = data['data']['shortTitle']
            result['title'] = data['data']['title']
            result['formatted_citation'] = data['formatted']
            result['access_uri'] = data['data']['url']

        return result

    def _zotero_api_result(self):
        api = zotero.Zotero(self.library_id, self.library_type)
        results = api.item(self.item_id, format='json')
        formatted = api.item(self.item_id, content='bib')
        results['formatted'] = formatted

        return results
