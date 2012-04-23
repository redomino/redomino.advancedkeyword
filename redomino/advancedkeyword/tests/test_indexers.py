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

from redomino.advancedkeyword.tests.base import TestCase


class TestIndexers(TestCase):
    """ Check if the customized plone indexer Subject works properly
    """

    def test_subjects1(self):
        """ redomino -> redomino"""
        front_page = self.portal['front-page']

        front_page.setSubject(['redomino'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino',))

    def test_subjects2(self):
        """ redomino.prodotti.recatalog -> redomino, redomino.prodotti, redomino.prodotti.recatalog"""
        front_page = self.portal['front-page']

        front_page.setSubject(['redomino.prodotti.recatalog'])
        front_page.reindexObject()
        self.assertEqual(set(self.portal.portal_catalog.uniqueValuesFor('Subject')), set(('redomino', 'redomino.prodotti', 'redomino.prodotti.recatalog')))

    def test_subjects3(self):
        """ redomino.prodotti.recatalog, redomino.prova -> redomino, redomino.prova, redomino.prodotti, redomino.prodotti.recatalog 
        """
        front_page = self.portal['front-page']

        front_page.setSubject(['redomino.prodotti.recatalog', 'redomino.prova'])
        front_page.reindexObject()
        self.assertEqual(set(self.portal.portal_catalog.uniqueValuesFor('Subject')), set(('redomino', 'redomino.prova', 'redomino.prodotti', 'redomino.prodotti.recatalog')))

    def test_subjects4(self):
        """ redomino, redomino. -> redomino"""
        front_page = self.portal['front-page']

        front_page.setSubject(['redomino', 'redomino.'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino',))

    def test_subjectsi5(self):
        """ redomino..pippo. -> redomino, pippo"""
        front_page = self.portal['front-page']

        front_page.setSubject(['redomino..pippo.'])
        front_page.reindexObject()
        self.assertEqual(self.portal.portal_catalog.uniqueValuesFor('Subject'), ('redomino', 'redomino.pippo'))




def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIndexers))
    return suite


