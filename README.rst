=====================
 Tau SelectorStrings
=====================

Introduction
============

The purpose of this component distribution is two-fold; to provide a useful
way of configuring clusters of strings to be presented in a dropdown list, and
to teach others how to create new ZCML directives.  The code has been
carefully documented to make it clear how it works.

My need for selectorstrings comes from another component I'm designing for
presenting collections of various files as a Zope folder.  I wanted to allow
the developer who adds an instance of this document folder, using the ZMI
(Zope Management Interface), to pick from a list of directories.  I did not
want them to be able to enter arbitrary directories, partly as a security
precaution and partly to prevent typing errors.

This resulted in the following ZCML directive::

    <selectorstring cluster="sitedocs"
        label="Public Documents"
        value="/usr/share/public/"
        />

    <selectorstring cluster="sitedocs"
        label="Family Photos"
        value="/home/jeff/photos/"
        />

And you can add more, using the same or difference cluster name and the
strings will be available as a Zope vocabulary under that cluster name.

One drawback is that each such simple directive repeats the cluster name
repeatedly.  So next I created a complex (nested) directive to factor out the
cluster name::

    <selectorcluster name="sitedocs">

        <selectorstring
            label="Public Documents"
            value="/usr/share/public/"
            />

        <selectorstring
            label="Family Photos"
            value="/home/jeff/photos/"
            />

    </selectorcluster>

.. sidebar:: Obtaining Development Versions

   In addition to the PyPI downloads, the development version of this
   component is available via its `project on Github`_.

.. _`project on Github`: https://github.com/xanalogica/tau.selectorstrings#egg=tau.selectorstrings-dev


Steps to Creating a New ZCML Directive
======================================

ZCML directives come in two flavors, simple and complex.  A simple directive
stands alone but a complex one supports grouping by containing one or more
other ZCML directives.

A new ZCML directive, either simple or complex, is described by four
pieces:

  1. its name
  2. the namespace it belongs to
  3. the schema
  4. its directive handler

The piece that ties these all together is the declaration of the (simple-kind
of) directive in the *meta.zcml* file::

    <meta:directive
        name="selectorstring"
        schema=".interfaces.ISelectorStringDirective"
        handler=".zcml_directives.selectorstring_SimpleDirectiveHandler"
        />

That takes care of declaring the name of the new directive and placing that
name into the "zope" namespace.  It could have placed it into the "browser"
namespace or some other space that would make organizational sense.

To declare a complex-kind of directive::

    <meta:complexDirective
        name="selectorcluster"
        schema=".interfaces.ISelectorClusterDirective"
        handler=".zcml_directives.selectorcluster_ComplexDirectiveHandler"
        >

        <meta:subdirective
            name="selectorstring"
            schema=".interfaces.ISelectorStringSubdirective"
            />

    </meta:complexDirective>


Using Your ZCML Directive
=========================

Like any ZCML directive, you place it into a configure.zcml file or some other
file included your the top-level ``site.zcml`` configuration file::

    <configure
        xmlns="http://namespaces.zope.org/zope">

        <selectorstring cluster="sitedocs"
            label="Public Documents"
            value="/usr/share/public/"
            />

    </configure>

Before the directive is recognized you **must** be sure that its definition in
its ``meta.zcml`` gets included into the top-level ``site.zcml`` file.  This
is done by placing into your ``buildout.cfg`` file for your *Zope2_instance*
part the following::

    zcml += tau.selectorstrings-meta

This causes the *plone.recipe.zope2instance* recipe to create a 'slug' file
under your ``parts/Zope2_instance/etc/package-includes/`` that does nothing but
include your ``tau/selectorstrings/meta.zcml`` file.  This inclusion happens
because of the following directive automatically placed into your
etc/site.zcml file by the recipe::

    <include files="package-includes/*-meta.zcml" />
