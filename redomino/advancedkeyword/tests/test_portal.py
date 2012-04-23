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


class TestPortal(TestCase):
    """ Check if js, css, etc are correctly registered
    """

    def test_js(self):
        """ dynatree plugin"""
        portal_javascripts = self.portal.portal_javascripts
        resource_ids = [item.getId() for item in portal_javascripts.resources]

        self.assertTrue('++resource++redomino.advancedkeyword.resources/jquery.keywordtree.js' in resource_ids)
        self.assertTrue('++resource++redomino.advancedkeyword.resources/subjectkeywordtree.js' in resource_ids)

    def test_css(self):
        """ Css resources loaded? """
        portal_css = self.portal.portal_css
        resource_ids = [item.getId() for item in portal_css.resources]

        self.assertTrue('++resource++redomino.advancedkeyword.resources/jquery.keywordtree.css' in resource_ids)

    def test_actions(self):
        """ Test portal actions """
        portal_actions = self.portal.portal_actions
        self.assertTrue('keywords' in  [item['id'] for item in portal_actions.listActionInfos()])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortal))
    return suite


