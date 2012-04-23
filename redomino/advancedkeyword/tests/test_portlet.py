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


from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from redomino.advancedkeyword.portlets import keywordportlet

from redomino.advancedkeyword.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc-tag1')
        self.portal.invokeFactory('Document', 'doc-tag2')
        doc1 = self.portal['doc-tag1']
        doc2 = self.portal['doc-tag2']
        doc1.setSubject(['supertag.subtag1','supertag1.subtag2'])
        doc2.setSubject(['supertag1.subtag3','supertag.subtag4'])
        doc1.reindexObject()
        doc2.reindexObject()

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='redomino.advancedkeyword.KeywordPortlet')
        self.assertEquals(portlet.addview,
                          'redomino.advancedkeyword.KeywordPortlet')

    def test_interfaces(self):
        portlet = keywordportlet.Assignment('myportlet', 'supertag')
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))
        

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='redomino.advancedkeyword.KeywordPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0],
                                   keywordportlet.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = keywordportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, keywordportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assignment = keywordportlet.Assignment('myportlet','supertag')

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, keywordportlet.Renderer))
        childrenTags = [item[1] for item in renderer.getChildrenTags('supertag')]

        self.assertTrue('subtag1' in childrenTags)
        self.assertTrue('subtag4' in childrenTags)
        self.assertFalse('subtag2' in childrenTags)

class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc-tag1')
        self.portal.invokeFactory('Document', 'doc-tag2')
        doc1 = self.portal['doc-tag1']
        doc2 = self.portal['doc-tag2']
        doc1.setSubject(['supertag.subtag1','supertag1.subtag2','supertag.subtag1.subsubtag'])
        doc2.setSubject(['supertag1.subtag3','supertag.subtag4'])
        doc1.reindexObject()
        doc2.reindexObject()

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or keywordportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal,
                          assignment=keywordportlet.Assignment('myportlet', 'supertag'))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
	self.assertTrue('Subject=supertag' in output)
	self.assertTrue('Subject=supertag.subtag1' in output)
	self.assertTrue('Subject=supertag.subtag4' in output)
	self.assertFalse('Subject=supertag1.subtag2' in output)
	self.assertFalse('Subject=supertag1.subtag3' in output)
	self.assertFalse('Subject=supertag.subtag1.subsubtag' in output)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
