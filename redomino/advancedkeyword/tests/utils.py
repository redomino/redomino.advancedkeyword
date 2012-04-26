from zope.site.hooks import setSite

from Products.ZCTextIndex.ParseTree import ParseError


def create_context():
    context = DummyContext()
    setSite(context)
    return context


class DummyContext(object):

    def __init__(self):
        self.__name__ = 'dummy'
        self.__parent__ = None

    def getSiteManager(self):
        return self

    def queryUtility(*args, **kwargs):
        return None


class DummyTool(object):

    def __init__(self, name):
        self.name = name


class DummyType(object):

    def __init__(self, title):
        self.title = title

    def Title(self):
        return self.title


class DummyTypeTool(dict):

    def __init__(self):
        self['Document'] = DummyType('Page')
        self['Event'] = DummyType('Event')

    def listContentTypes(self):
        return self.keys()


class Response(dict):

    def getHeader(self, value):
        return 'header %s' % value


class Request(dict):

    debug = False
    response = Response()

    def __init__(self, form=None):
        self.form = form


class Brain(object):

    Title = 'BrainTitle'
    is_folderish = True

    def __init__(self, rid):
        self.rid = rid

    def getPath(self):
        return self.rid


class DummyCatalog(dict):

    def __init__(self, values):
        self.indexes = {}
        for r in values:
            self[r] = Brain(r)

    def __call__(self, **values):
        if 'SearchableText' in values:
            st = values['SearchableText']
            if st.startswith('error'):
                raise ParseError
        return self.values()

    @property
    def _catalog(self):
        return self

    def getrid(self, value):
        return value in self and value or None

    def getIndex(self, name):
        return self.indexes[name]


class DummyContent(object):
    def __init__(self, title, subjects=[]):
        self.title = title
        self.subjects = subjects

    def Title(self):
        return self.title

    def Subject(self):
        return self.subjects
