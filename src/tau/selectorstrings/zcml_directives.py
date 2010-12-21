"""

   ZCML directives can be divided into two kinds; simple and complex.  A
   simple directive is a standalone XML tag.  A complex directive acts as a
   container of other ZCML directives, giving them context and allowing for
   the factoring out of redundant XML tags.

   A simple directive has a handler implemented as a simple function, which is
   called in the XML-tag closure phase.

   A complex directive has a handler that is a class instantiated at XML-tag
   open with the XML tag attributes, and the instance called at XML tag
   closure.

   In this module we'll implement one of each.

   For the simple directive::

      <selectorstring
          cluster="sitedocs"
          label="Public Materials"
          value="/usr/share/public"
          />

   For the complex directive::

      <selectorcluster name="sitedocs">
          <selectorstring label="Public Materials", value="/usr/share/public" />
          <selectorstring label="For-Pay Materials", value="/home/jeff/works" />
          <selectorstring label="Family Photos", value="/home/jeff/photos" />
      </selection>

   from zope.schema import Choice
   class ILibrary(Interface):
       sitedocs = Choice(
           title=u"Path to Site Documents",
           vocabulary="vocabname"
           )
"""
from zope.interface import implements, alsoProvides
from zope.component import queryUtility, provideUtility
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from .interfaces import ISelectorStringDirective, ISelectorClusterDirective, IClusterOfSelectors

import logging
log = logging.getLogger("tau.selectorstrings")


class selectorcluster_ComplexDirectiveHandler(object):

    def __init__(self, _context, name):
        """
            Takes as arguments any attributes of the complex (outer) directive.
        """
        self.__context = _context
        self.name = name

        _context.action( # register an action to occur at the end of the configuration process
            discriminator=('selectorcluster', name),  # must be unique!
            callable=self.deferred__instantiate_cluster,
            args=(_context, name),
            )

    def deferred__instantiate_cluster(self, _context, name):
        log.info("deferred__instantiate_cluster fired for cluster %r!" % name)

        self.cluster = queryUtility(IClusterOfSelectors, name=name)
        if self.cluster is None:
            log.info("No such cluster as %r, creating one" % name)
            self.cluster = ClusterOfSelectors(name)
            provideUtility(self.cluster, provides=IClusterOfSelectors, name=name)

            def SelectorFactory(context):
                cluster = queryUtility(IClusterOfSelectors, name=name)
                return cluster
            alsoProvides(SelectorFactory, IVocabularyFactory)
            provideUtility(SelectorFactory, provides=IVocabularyFactory, name=name)

    def selectorstring(self, _context, value, label=None):

        _context.action( # register an action to occur at the end of the configuration process
            discriminator=('selectorstring', self.name, value, label),  # must be unique!
            callable=self.deferred__append_selector,
            args=(_context, value, label),
            )

    def deferred__append_selector(self, _context, value, label):
        self.cluster.register(value, label)

    def __call__(self):
        """
            Called when the complex directive is *** empty ***.
        """
        return ()


def selectorstring_SimpleDirectiveHandler(_context, cluster, value, label=None):
    """Handler of a simple ZCML directive.

       NOTE: A handler does NOT execute an action immediately but instead
       registers an action to occur at the end of the configuration process.
       This is because the system should go through all of the configuration
       first, detecting possible conflicts and implementing possible
       overrides.  Only after the configuration is fully determined are the
       registered actions performed.

       Takes as arguments any attributes of the simple directive, after they
       have been validated by Zope against the directive's schema.
    """

    def deferred__append_selector(_context, clustername, value, label):
        """
            Each time we see a selector directive, append the choice to the existing vocabulary.
        """

        cluster = queryUtility(IClusterOfSelectors, name=clustername)
        if cluster is None:
            log.info("No such cluster as %r, creating one" % clustername)
            cluster = ClusterOfSelectors(clustername)
            provideUtility(cluster, provides=IClusterOfSelectors, name=clustername)

            def SelectorFactory(context):
                cluster = queryUtility(IClusterOfSelectors, name=clustername)
                return cluster
            alsoProvides(SelectorFactory, IVocabularyFactory)
            provideUtility(SelectorFactory, provides=IVocabularyFactory, name=clustername)

        cluster.register(value, label)

    _context.action( # register an action to occur at the end of the configuration process
        discriminator=('selectorstring', cluster, value, label),  # must be unique!
        callable=deferred__append_selector,
        args=(_context, cluster, value, label),
        )


class SelectorTerm(SimpleTerm):

    def __repr__(self):
        return "%s(token=%r, value=%r, title=%r)" % (
            self.__class__.__name__, self.token, self.value, self.title)


class ClusterOfSelectors(SimpleVocabulary):
    """A iterable container of selector strings ***for a particular cluster***.
    """
    implements(IClusterOfSelectors)

    def __init__(self, clustername):
        SimpleVocabulary.__init__(self, [])
        self.clustername = clustername

    def __repr__(self):
        return "%s(%r, id=%r)" % (self.__class__.__name__, self.clustername, id(self))

    @classmethod
    def createTerm(cls, *args):
        return SelectorTerm(*args)

    def register(self, value, label=None):
        title = value if label is None else label
        token = str(value)

        term = self.createTerm(value, token, title)

        self._terms.append(term)
        self.by_value[term.value] = term
        self.by_token[term.token] = term

        if len(self.by_value) != len(self.by_token) != len(self._terms):
            raise ValueError(
                'Adding selector (value=%r, label=%r) resulted in a duplicate entry.' % (value, label))
