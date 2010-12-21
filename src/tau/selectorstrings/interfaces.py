##############################################################################
#
# Copyright (c) 2010 Tau Productions Inc.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Declaration of various object interfaces.
"""

from zope.interface import Interface
from zope.schema import TextLine

class ISelectorStringDirective(Interface):
    """Schema for a simple, single ZCML directive for declaring a vocabulary of strings.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorstring
             cluster="docfolders"
             label="Personal Photos"
             value="/home/jeff/photos/"
             />
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


class ISelectorClusterDirective(Interface):
    """Schema for a complex, nested ZCML directive for declaring a vocabulary of strings.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorcluster                 <---- just the outer directive
             name="sitevids">

             <selectorstring
                 label="Delta Path"
                 value="/delta/"
                 />

             <selectorstring
                 label="Omega Path"
                 value="/omega/"
                 />

         </selectorcluster>
    """

    name = TextLine(
        title=u"Cluster",
        description=u"The name of this cluster for grouping labels/values.",
        required=True,
        )


class ISelectorStringSubdirective(Interface):
    """Schema for the ZCML directives nested inside the top-level cluster directive.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorcluster
             name="sitevids">

             <selectorstring              <---- just the inner directive
                 label="Delta Path"
                 value="/delta/"
                 />

             <selectorstring
                 label="Omega Path"
                 value="/omega/"
                 />

         </selectorcluster>
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


class IClusterOfSelectors(Interface):
    """An empty interface for tracking registered clusters in the registry.

       We tag instances of our Cluster class with this interface so we can
       retrieve them again from Zope's interface registry.  This retrieval
       also uses a name along with the interface where the name reflects the
       name of the cluster.

       Example::

         cluster = queryUtility(IClusterOfSelectors, name=clustername)
    """
