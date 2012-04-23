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

from zope.component import getMultiAdapter
from redomino.advancedkeyword.tests.base import TestCase


class TestKeywordmap(TestCase):
    """
    """

    def afterSetUp(self):
        super(TestKeywordmap, self).afterSetUp()
        self.sitemap = getMultiAdapter((self.portal, self.portal.REQUEST), name='keywordsmap')

    def test_enabled_disabled_view(self):
        """ Test keywordmapenabled view. This view is used by the 'Keywords map' action """
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = True
        self.assertTrue(self.portal.restrictedTraverse('keywordmapenabled')())

        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = False
        self.assertFalse(self.portal.restrictedTraverse('keywordmapenabled')())

    def test_enabled(self):
        """
        If the keyword map sitemap is disabled throws a 404 error.
        """
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = True

        self.sitemap()
        self.assertTrue('Subjects map' in self.portal())

    def test_disabled(self):
        """
        If the keyword map sitemap is disabled throws a 404 error.
        """
        from zope.publisher.interfaces import INotFound
        from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema
        IKeywordMapSchema(self.portal).keywordmapenabled = False
        self.assertFalse('Subjects map' in self.portal())

        try:
            self.sitemap()
        except Exception, e:
            # zope2 and repoze.zope2 use different publishers and raise
            # different exceptions. but both implement INotFound.
            self.assertTrue(INotFound.providedBy(e))
        else:
            self.fail('The disabled sitemap view has to raise NotFound!')



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestKeywordmap))
#    suite.addTest(makeSuite(TestKeywordGenerator))
    return suite


