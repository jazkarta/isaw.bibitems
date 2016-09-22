from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IEditForm, IAddForm
from zope import schema
from zope.interface import Interface
from zope.interface import provider
from . import MessageFactory as _


class IISAWBibItemsLayer(Interface):
    pass


@provider(IFormFieldProvider)
class IBibliographicItem(model.Schema):

    title = schema.TextLine(
        title=_(u"Short Title"),
        description=_(u"The short title of the bibliographic reference."),
    )

    description = schema.Text(
        title=_(u'Summary'),
        description=_(u'Used in item listings and search results.'),
        required=False,
        missing_value=u'',
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

    form.omitted('description')
    form.no_omit(IEditForm, 'description')
    form.no_omit(IAddForm, 'description')


class IBibliographicURLIFetcher(Interface):

    def fetch(uri):
        """Returns bibliographic data (in a dictionary) given a URI for a bibliographic
        resource"""
