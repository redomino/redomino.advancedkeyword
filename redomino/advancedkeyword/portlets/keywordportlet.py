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

from Acquisition import aq_inner
from Acquisition import aq_parent

from zope.interface import implements
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.component import getMultiAdapter

from z3c.form import form
from z3c.form import field
from z3c.form import button

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from redomino.advancedkeyword import _

from plone.z3cform import layout

class PortletFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
       portlets layout.
    """

    index = ViewPageTemplateFile('portlets_layout.pt')


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
                             vocabulary=u"redomino.advancedkeyword.vocabularies.Keywords",
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

class AddForm(form.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    implements(IPortletAddForm)

    fields = field.Fields(IKeywordPortlet)
    label = _(u'label_add_keywordportlet', default=u"Add keyword portlet")

    def create(self, data):
        return Assignment(**data)

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        addview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(addview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''

AddFormView = layout.wrap_form(AddForm, PortletFormWrapper)

class EditForm(form.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    implements(IPortletEditForm)

    fields = field.Fields(IKeywordPortlet)

    label = _(u'label_modify_keyword_portlet', default=u"Modify keyword portlet")

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = _(u'status_changes_saved', default="Changes saved")
        else:
            self.status = _(u'status_no_changes', default=u"No changes")

        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''

EditFormView = layout.wrap_form(EditForm, PortletFormWrapper)
