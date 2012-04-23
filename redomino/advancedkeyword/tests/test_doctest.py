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


import unittest
import doctest
from zope.component import testing

#from zope.testing import doctestunit
#from zope.component import testing, eventtesting

#from Testing import ZopeTestCase as ztc

#from redomino.advancedkeyword.tests import base


def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
#        ztc.ZopeDocFileSuite(
#            'README.txt', package='redomino.advancedkeyword',
#            test_class=base.FunctionalTestCase,
#            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
#                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        doctest.DocTestSuite(
            module='redomino.advancedkeyword.indexers',
            setUp=testing.setUp, tearDown=testing.tearDown),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
