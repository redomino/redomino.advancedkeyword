# Copyright (c) 2011 Redomino srl (http://redomino.com)
# Authors: Davide Moro <davide.moro@redomino.com>
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


class TestTreeKeywords(TestCase):
    """ Check if the tree keywords works fine
    """

    def _getTreeBrowserView(self,all_kw, selecteded_kw):
        from redomino.advancedkeyword.browser.keywords import KWGenerator
        class MockKeywordsKW(KWGenerator):
            def get_all_kw(self):
                return all_kw
            def get_selected_kw(self):
                return selecteded_kw
        return MockKeywordsKW(self.portal, self.portal.REQUEST)


    def test_keywords1(self):
        """ 
            Just one subject selected:

                * redomino

            Output structure:

                * redomino
        """
        l = ['redomino']
        data = self._getTreeBrowserView(l, l)()
        self.assertEquals(len(data), 1)
        self.assertFalse(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(data[0]['children'], [])

    def test_keywords2(self):
        """ 
            Two subjects selected:

                * redomino
                * redomino.prova.qualcosa

            Output:
 
               * redomino (selecteded)
               * redomino.prova (selecteded)
               * redomino.prova.qualcosa (selecteded)
        """
        l = ['redomino', 'redomino.prova.qualcosa']
        data = self._getTreeBrowserView(l, l)()

        self.assertEquals(len(data), 1)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)

        self.assertTrue(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[0]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(len(data[0]['children'][0]['children']), 1)

        self.assertFalse(data[0]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'][0]['children'], [])

    def test_keywords3(self):
        """ 
            It's just one subject (an entire branch):

                * redomino.prova.qualcosa

            Output:
 
               * redomino (selecteded)
               * redomino.prova (selecteded)
               * redomino.prova.qualcosa (selecteded)
        """

        l = ['redomino.prova.qualcosa']
        data = self._getTreeBrowserView(l, l)()

        self.assertEquals(len(data), 1)
        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'redomino')
        self.assertEquals(data[0]['keyword'], 'redomino')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)

        self.assertTrue(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[0]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(len(data[0]['children'][0]['children']), 1)

        self.assertFalse(data[0]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[0]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'][0]['children'], [])

    def test_keywords4(self):
        """ 
            Subjects:
            
            * pippo
            * redomino
            * redomino.prova.qualcosa

            Output (all tree nodes selecteded):

            * pippo
            * redomino
            * redomino.prova
            * redomino.prova.qualcosa
        """

        l = ['redomino', 'redomino.prova.qualcosa', 'pippo']
        data = self._getTreeBrowserView(l, l)()

        self.assertEquals(len(data), 2)
        self.assertFalse(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(data[0]['children'], [])

        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], True)
        self.assertEquals(len(data[1]['children']), 1)

        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], True)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)

        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])


    def test_keywords5(self):
        """ 
            All Subjects:
            
            * redomino
            * redomino.prova.qualcosa
            * pippo
            * pippo.pluto

            case 1 selected:
            
            * redomino
            * redomino.prova.qualcosa
            * pippo

            case 2 selected:
            
            * pippo.pluto

            Output for case 1:

            * redomino (selecteded)
            * pippo (selecteded)
            * pippo.pluto (UNselectedED)
            * redomino.prova (selecteded)
            * redomino.prova.qualcosa (selecteded)

            Output for case 2:

            * redomino (UNselectedED)
            * pippo (selecteded)
            * pippo.pluto (selecteded)
            * redomino.prova (UNselectedED)
            * redomino.prova.qualcosa (UNselectedED)
        """

        l = ['redomino.prova.qualcosa', 'pippo', 'pippo.pluto']
        l2 = ['redomino.prova.qualcosa', 'pippo']
        l3 = ['pippo.pluto']

        data = self._getTreeBrowserView(l, l2)()

        self.assertEquals(len(data), 2)

        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)

        self.assertFalse(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'pippo.pluto')
        self.assertEquals(data[0]['children'][0]['keyword'], 'pluto')
        self.assertEquals(data[0]['children'][0]['selected'], False)
        self.assertEquals(data[0]['children'][0]['children'], [])

        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], True)
        self.assertEquals(len(data[1]['children']), 1)

        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], True)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)

        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], True)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])

        # another
        data = self._getTreeBrowserView(l, l3)()

        self.assertEquals(len(data), 2)

        self.assertTrue(data[0]['is_folder'])
        self.assertEquals(data[0]['full_keyword'], 'pippo')
        self.assertEquals(data[0]['keyword'], 'pippo')
        self.assertEquals(data[0]['selected'], True)
        self.assertEquals(len(data[0]['children']), 1)

        self.assertFalse(data[0]['children'][0]['is_folder'])
        self.assertEquals(data[0]['children'][0]['full_keyword'], 'pippo.pluto')
        self.assertEquals(data[0]['children'][0]['keyword'], 'pluto')
        self.assertEquals(data[0]['children'][0]['selected'], True)
        self.assertEquals(data[0]['children'][0]['children'], [])

        self.assertTrue(data[1]['is_folder'])
        self.assertEquals(data[1]['full_keyword'], 'redomino')
        self.assertEquals(data[1]['keyword'], 'redomino')
        self.assertEquals(data[1]['selected'], False)
        self.assertEquals(len(data[1]['children']), 1)

        self.assertTrue(data[1]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['full_keyword'], 'redomino.prova')
        self.assertEquals(data[1]['children'][0]['keyword'], 'prova')
        self.assertEquals(data[1]['children'][0]['selected'], False)
        self.assertEquals(len(data[1]['children'][0]['children']), 1)

        self.assertFalse(data[1]['children'][0]['children'][0]['is_folder'])
        self.assertEquals(data[1]['children'][0]['children'][0]['full_keyword'], 'redomino.prova.qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['keyword'], 'qualcosa')
        self.assertEquals(data[1]['children'][0]['children'][0]['selected'], False)
        self.assertEquals(data[1]['children'][0]['children'][0]['children'], [])



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTreeKeywords))
    return suite


