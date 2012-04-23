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


from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from redomino.advancedkeyword import _
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

class IKeywordPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    name = schema.TextLine(
            title=_(u"label_keywordportlet_title", default=u"Title"),
            description=_(u"help_keywordportlet_title",
                          default=u"The title of the keyword portlet. If empty, it will be used 'Search by {tag}'"),
            default=u"",
            required=True)

    selectedtag = schema.Choice(title=_(u"label_tags", default=u"Tags"),
                             vocabulary=u"plone.app.vocabularies.Keywords",
                             required=True,
                             )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IKeywordPortlet)
    name = u""
    selectedtag = u""

    def __init__(self, name = '', selectedtag = ''):
        self.name = name
        self.selectedtag = selectedtag

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.name:
            return self.name
        else:
            return _(u'label_keywordportlet_deftitle', default='Search for ${tag}', mapping={'tag': self.selectedtag})


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    def title(self):
        return self.data.title

    @property
    def available(self):
        return bool(self._data())

    render = ViewPageTemplateFile('keywordportlet.pt')

    def getChildrenTags(self):
        results = self._data()
        return results

    @memoize
    def _data(self):
        tag = self.data.selectedtag
        vocab_factory = getUtility(IVocabularyFactory, "plone.app.vocabularies.Keywords")
        vocab = vocab_factory(self.context)
        tag_level = len(tag.split('.'))+1
        results = [(term.value, term.value.split('.')[-1]) for term in vocab if term.value.startswith(tag) and len(term.value.split('.')) == tag_level]
        return results

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IKeywordPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IKeywordPortlet)
