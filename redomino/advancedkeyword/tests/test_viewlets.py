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

from redomino.advancedkeyword.tests.base import FunctionalTestCase
from zope.component import getMultiAdapter

from zope.viewlet.interfaces import IViewlet, IViewletManager



class TestViewlets(FunctionalTestCase):
    """ Verifichiamo se la viewlet visualizza correttamente le keyword
    """

    def afterSetUp(self):
        super(TestViewlets, self).afterSetUp()
        portal = self.portal
        fp = portal['front-page']
        request = self.portal.REQUEST
        view = portal.restrictedTraverse('@@plone')

        from plone.app.layout.globals.interfaces import IViewView
        from zope.interface import alsoProvides
        alsoProvides(view, IViewView)
        manager = getMultiAdapter((fp, request, view), IViewletManager,
                        name=u'plone.belowcontent')

        # IT DOES NOT WORK: see http://stackoverflow.com/questions/5628089/how-to-access-views-defined-with-a-specific-plone-browserlayer-in-test-cases 
        #from redomino.advancedkeyword.browser.interfaces import IRedominoAdvancedKeywordLayer
        #from zope.interface import directlyProvides
        #directlyProvides(request, IRedominoAdvancedKeywordLayer)
        viewlet = getMultiAdapter((fp, request, view, manager), IViewlet,
                        name=u'plone.belowcontenttitle.keywordstest')

        self.fp = fp
        self.viewlet = viewlet


    def test_right_viewlet(self):
        """ Test right viewlet """
        from redomino.advancedkeyword.browser.viewlets import KeywordsViewlet

        # ok, it is our customized viewlet
        self.assertTrue(isinstance(self.viewlet, KeywordsViewlet))

    def test_keyword1(self):
        """ 'redomino' -> 'redomino' """
        fp = self.fp
        viewlet = self.viewlet
        fp.setSubject(['redomino'])
        fp.reindexObject()

        viewlet.update()
        self.assertEquals(set(['redomino']), set(viewlet.subjects))

    def test_keyword2(self):
        """ 'redomino','pippo.prova' -> 'redomino', 'pippo', 'pippo.prova' """
        fp = self.fp
        viewlet = self.viewlet
        fp.setSubject(['redomino', 'pippo.prova'])
        fp.reindexObject()
        viewlet.update()

        self.assertEquals(set(['redomino', 'pippo', 'pippo.prova']), set(viewlet.subjects))



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestViewlets))
    return suite


