import logging
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('isaw.bibitems')

logger = logging.getLogger('isaw.bibitems')
