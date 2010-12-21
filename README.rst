=====================
 Tau SelectorStrings
=====================

Introduction
============


Steps to Creating a Simple ZCML Directive
=========================================

ZCML directives come in two flavors, simple and complex.  A simple directive
stands alone but a complex one supports grouping by containing one or more
other ZCML directives.

A new ZCML directive, either simple of complex, is described by four
pieces:

  1. its name
  2. the namespace it belongs to
  3. the schema
  4. its directive handler

The piece that ties these all together is the declaration of the directive in
your *meta.zcml* file::

    <meta:directives namespace="http://namespaces.zope.org/zope">

        <meta:directive
            name="selector"
            schema=.metadirectives.IAdapterDirective
            handler=".metaconfigure.adapterDirective"
            />

    </meta:directives>

That takes care of declaring the name of the new directive and placing that
name into the "zope" namespace.  You could have placed it into the "browser"
namespace or some other space that would make organizational sense.

To define the new directive's schema or set of NAME=VALUEs that it
accepts/requires, you create an interface definition.

 FILE: metadirectives.py
 |
PythonIdentifier
GlobalObject
Tokens
Path
Bool
MessageID
 |



Using Your ZCML Directive
=========================

Like any ZCML directive you place it into a configure.zcml file or some other
file included into the top-level site.zcml configuration file::

    <configure
        xmlns="http://namespaces.zope.org/zope">

        <selection
            cluster="sitedocs"
            label="Jeff's Site Docs"
            value="/home/jeff/sitedocs/"
            />

        <selection
            cluster="sitedocs"
            label="Mary's Site Docs"
            value="/home/mary/sitedocs/"
            />

    </configure>

Before the directive is recognized you must be sure that its definition in
your meta.zcml gets included into the top-level site.zcml file.
