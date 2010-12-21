from zope.interface import Interface
from zope.schema import TextLine

class ISelectorClusterDirective(Interface):
    """
    """

    name = TextLine(
        title=u"Cluster",
        description=u"The name of this cluster for grouping labels/values.",
        required=True,
        )

class ISelectorStringSubdirective(Interface):
    """
    """

    label = TextLine(
        title=u"Label",
        description=u"An optional label to display to the user making the choice.",
        required=False,
        )

    value = TextLine(
        title=u"Value",
        description=u"A string representing the actual value used internally.",
        required=True,
        )

class ISelectorStringDirective(Interface):
    """
    """

    cluster = TextLine(
        title=u"Cluster",
        description=u"The name of the cluster under which to group this label/value.",
        required=False,
        )

    label = TextLine(
        title=u"Label",
        description=u"An optional label to display to the user making the choice.",
        required=False,
        )

    value = TextLine(
        title=u"Value",
        description=u"A string representing the actual value used internally.",
        required=True,
        )

class IClusterOfSelectors(Interface):
    """
    """
