# Copyright (c) 2012 Redomino srl (http://redomino.com)
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
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

class KeywordsVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "Subject" index

        >>> from redomino.advancedkeyword.tests.utils import DummyCatalog
        >>> from redomino.advancedkeyword.tests.utils import create_context
        >>> from redomino.advancedkeyword.tests.utils import DummyContent
        >>> from redomino.advancedkeyword.tests.utils import Request
        >>> from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex

        >>> context = create_context()

        >>> rids = ('/1234', '/2345', '/dummy/1234')
        >>> tool = DummyCatalog(rids)
        >>> context.portal_catalog = tool
        >>> index = KeywordIndex('Subject')
        >>> done = index._index_object(1,DummyContent('ob1', ['foo', 'bar', 'baz']), attr='Subject')
        >>> done = index._index_object(2,DummyContent('ob2', ['blee', 'bar']), attr='Subject')
        >>> tool.indexes['Subject'] = index
        >>> vocab = KeywordsVocabulary()
        >>> result = vocab(context)
        >>> result.by_token.keys()
        ['blee', 'baz', 'foo', 'bar']
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        self.catalog = getToolByName(context, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('Subject')
        items = [SimpleTerm(i, i.decode('utf-8').encode('ascii', 'ignore'), i) for i in index._index]
        return SimpleVocabulary(items)

KeywordsVocabularyFactory = KeywordsVocabulary()
