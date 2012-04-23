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

from zope.publisher.interfaces import NotFound
from zope.publisher.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import queryUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from plone.i18n.normalizer.interfaces import IIDNormalizer

from redomino.advancedkeyword.config import KEYWORD_SEPARATOR
from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema

class KWGenerator(BrowserView):
    """Keyword tree generator baseclass"""

    def get_all_kw(self):
        raise NotImplementedError

    def get_selected_kw(self):
        raise NotImplementedError

    def _getKWTree(self):
        out = {}
        for item in self.get_all_kw():
            currentdict = out
            for kw in item.split(KEYWORD_SEPARATOR):
                currentdict = currentdict.setdefault(kw, {})
        return out

    def __call__(self):
        return self._getTree(self._getKWTree())

    def _is_selected(self,prefix):
        for kw in self.get_selected_kw():
            if kw.startswith(prefix): return True
        return False

    @memoize
    def getIdNormalizer(self):
        return queryUtility(IIDNormalizer)

    def _getTree(self, d, prefix = None):
        if not d:
            return []
        idnormalizer = self.getIdNormalizer()
        out = []
        keys = sorted(d.keys(), key=lambda s: s.lower())
        for k in keys:
            newprefix = prefix and KEYWORD_SEPARATOR.join([prefix,k]) or k
            children = self._getTree(d[k], newprefix)
            out.append({'full_keyword': newprefix,
                        'keyword': k,
                        'children': children,
                        'selected': self._is_selected(newprefix),
                        'is_folder':bool(len(children)),
                        'id': idnormalizer.normalize(newprefix)
                         })
        return out

class KeywordsMapGenerator(KWGenerator):
    """Keyword tree generator for Keyword Map

       - all the subjects
       - It doesn't matter which keyword is selected
    """

    def get_all_kw(self):
        catalog = getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_tools').catalog()
        return catalog.uniqueValuesFor('Subject')


    def get_selected_kw(self):
        return []

class KeywordsWidgetGenerator(KWGenerator):
    """Keyword tree generator for Keyword widget

       - all the subjects
       - the subject in the context
    """

    def get_all_kw(self):
        field = self.context.getField('subject')
        return self.context.collectKeywords(field.getName(), field.accessor, field.widget.vocab_source)

    @memoize
    def get_selected_kw(self):
        return self.context.Subject()


class KeywordsMap(BrowserView):
    """ A keyword maps of the whole site """

    template = ViewPageTemplateFile('templates/keywordmap.pt')

    def getTree(self):
        gen = getMultiAdapter((self.context, self.request), name=u'keywordsmapgenerator')
        return gen()
        
    def __call__(self):
        """Checks if the sitemap feature is enable and returns it."""
        portal = getMultiAdapter((self.context, self.request), name=u"plone_portal_state").portal()
        if not IKeywordMapSchema(portal).keywordmapenabled:
            raise NotFound(self.context, 'keywordsmap', self.request)
        return self.template()




