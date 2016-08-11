from five import grok
from json import dumps
from urlparse import urlparse
from zope.component import queryUtility
from zExceptions import BadRequest
from plone.app.layout.navigation.interfaces import INavigationRoot
from ..interfaces import IBibliographicURLIFetcher


class JSONBiblographyDataFetcher(grok.View):
    grok.context(INavigationRoot)
    grok.name('fetch-bibliographic-data')
    grok.require('zope2.View')

    data = None

    def update(self):
        url = self.request.get('url')
        if not url:
            raise BadRequest('Missing request parameter "uri"')

        hostname = urlparse(url).hostname
        fetcher = queryUtility(IBibliographicURLIFetcher, name=hostname)
        if fetcher is None:
            self.data = {
                u"error": "Could not find biblographic fetcher for {}".format(
                    hostname
                ),
            }
            return

        self.data = fetcher.fetch(url)

    def render(self):
        res = self.request.response
        if u"error" in self.data:
            res.setStatus(500)
        if not self.data:
            self.data[u"error"] = u"Record not found"
            res.setStatus(404)

        res.setHeader('Content-Type', 'application/json; encoding=utf-8')
        return dumps(self.data)
