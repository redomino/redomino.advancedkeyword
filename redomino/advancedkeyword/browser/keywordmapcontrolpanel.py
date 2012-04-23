# Copyright (c) 2011 Redomino srl (http://redomino.com)
# Authors: Davide Moro <davide.moro@redomino.com> and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Bool
from zope.site.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from redomino.advancedkeyword import _

class IKeywordMapSchema(Interface):

    keywordmapenabled = Bool(title=_(u"label_keywordmapenabled", default=u"Enable KeywordMap"),
                       description=_(u"help_keywordmapenabled", default=u""),
                       default=False,
                       required=False)


class KeywordMapControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IKeywordMapSchema)

    def __init__(self, context):
        super(KeywordMapControlPanelAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.advancedkeyword_properties
        #self.encoding = pprop.advancedkeyword_properties.default_charset

    keywordmapenabled = ProxyFieldProperty(IKeywordMapSchema['keywordmapenabled'])

class KeywordMapControlPanel(ControlPanelForm):

    form_fields = form.FormFields(IKeywordMapSchema)

    label = _(u"label_keywordmapsettings", default=u"KeywordMap settings")
    description = _(u"help_keywordmapsettings", default=u"General editing settings.")
    form_name = _(u"label_keywordmapform", default=u"AdvancedKeyword settings")
