from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class IsawbibitemsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import isaw.bibitems
        xmlconfig.file(
            'configure.zcml',
            isaw.bibitems,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'isaw.bibitems:default')

ISAW_BIBITEMS_FIXTURE = IsawbibitemsLayer()
ISAW_BIBITEMS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ISAW_BIBITEMS_FIXTURE,),
    name="IsawbibitemsLayer:Integration"
)
ISAW_BIBITEMS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ISAW_BIBITEMS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IsawbibitemsLayer:Functional"
)
