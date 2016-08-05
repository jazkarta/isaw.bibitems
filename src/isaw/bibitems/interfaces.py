from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from . import MessageFactory as _


class IISAWBibItemsLayer(Interface):
    pass


class IBibliographicItem(model.Schema):

    title = schema.TextLine(
        title=_(u"Short Title"),
        description=_(u"The short title of the bibliographic reference."),
    )

    citation_detail = schema.TextLine(
        title=_(u"Citation Detail"),
        required=False,
    )

    formatted_citation = schema.TextLine(
        title=_(u"Formatted Citation"),
        required=False,
    )

    bibliographic_uri = schema.URI(
        title=_(u"Bibliographic URI"),
        description=_(u"This is a URI to an online bibliographic reference "
                      u"(e.g. zotero, worldcat, openlibrary, ...)."),
        required=False,
    )

    access_uri = schema.URI(
        title=_(u"Access URI"),
        description=_(u"This is a URI to access the identified resource."),
        required=False,
    )

    alternate_uri = schema.URI(
        title=_(u"Alternate URI"),
        description=_(u"This is an alternate URL for the identified "
                      u"resource."),
        required=False,
    )
