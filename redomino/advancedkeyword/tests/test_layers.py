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


class TestLayer(FunctionalTestCase):
    """ Test layers
    """


    def test_layer(self):
        """
        """
        from redomino.advancedkeyword.browser.interfaces import IRedominoAdvancedKeywordLayer
        from plone.browserlayer.utils import registered_layers

        self.assertTrue(IRedominoAdvancedKeywordLayer in registered_layers())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLayer))
    return suite


