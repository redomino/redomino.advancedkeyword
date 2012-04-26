redomino.advancedkeyword
========================

The ``redomino.advancedkeyword`` plugin aims to improve the keyword mechanism provided by Plone introducing *hierarchy* among keywords.
All the customizations introduced by redomino.advancedkeyword are made with backward compatibility in mind.
You can also use this plugin without pain when you need to migrate your contents: redomino.advancedkeyword still uses the standard ``subject`` field and the main work was made at frontend level
using javascript.

Note: having your javascript enabled is not required to use redomino.advancedkeyword.

What are the main problems of the old keyword management?
---------------------------------------------------------

Here is a list of problems:

* all the keywords are listed as a long, long plain list
* keywords are not semantically grouped

Here you can see the standard keyword widget how it is prompted to :

.. figure:: https://github.com/redomino/redomino.advancedkeyword/raw/master/docs/resources/keywordold.png
   :align: center

   Old keywords widgets.

As you can imagine the above edit widget is hard to use and difficult to manage.

How can AdvancedKeyword help you
--------------------------------

And now the advanced keyword widget with hierarchical management:

.. figure:: https://github.com/redomino/redomino.advancedkeyword/raw/master/docs/resources/keywordtree.png
   :align: center

   Keywords widget powered by redomino.advancedkeyword

The above image lets the keyword editor collapse/expand semantic groups of keywords, which makes it more suitable to manage large
sets of keywords as you can find in a large intranet.

You can also search for existing keywords through the existing tags.


How does it work?
=================

Hierarchy is introduced using the ``.`` (dot) character: it will be used as a keyword separator.
Why are we using the dot character and not another one? Because it is little used in keywords and it is easy to type.

Edit view
---------

If you use correctly the . separator, you will be able to create a keyword tree similar to the following one:

::

    [+] what [v]
        [+] what.doors [v]
            [+] what.doors.flat
            [+] what.doors.profiled
        [+] what.furniture
    [-] technology [v]
    ...

Clicking on the collapse or expand controls you can open or close keyword nodes.
If you click on a keyword that is a leaf, all its parents will be selected automatically; if you unselect a node, all the sub-keywords selected are automatically deselected.
So by the keyword editor you will be able to select single leafs or internal nodes.

You can add new keywords using the standard Plone control: nothing has changed. If you want to add one or more keywords then type something similar to the following example:

* what.furniture.outdoor
* etc

How keywords are shown on tagged contents
-----------------------------------------

If you choose the following keywords on a particular object:

* what.doors.flat
* technology.combined systems

the customized keywords viewlet will prompt the following links:

* what (clicking on this item you will be able to see all the products)
* what.doors (clicking on this item you will be able to see all the door related products)
* what.doors.flat (clicking on this item you will be able all the flat doors related products)
* technology
* technology.combined systems

This works because we provide a customized catalog indexer for keywords.

In the next release a new mechanism will be provided for changing the displayed keywords. For instance, if you don't like how "technology.combinened systems" looks like, you'll be able to edit it.

How to use AdvancedKeyword on an existing site
----------------------------------------------

At first you will see the javascript plugin with a plain keywords list, you should add the hierarchy level grouping keywords separated by dots characters: the Plone plugin named KeywordManager is your friend!

Other features
==============

Keyword map
-----------

Thanks to the keywords map you 're able to see the website's arguments structure.

How to see the arguments map of the site:

* portal_url/@@keywordsmap

Keywords portlet
----------------

This product also adds a new portlet: Keyword Portlet. In order to assign a new
instance of this portlet you will have to choose a "supertag" (or a namespace
tag). This supertag will be used to browse a list of all tags that are "first
child" of this tag. For ex. if your portal has these two contents::

    >>> doc1.Subjects()
    ['supertag','supertag1','supertag.subtag1','supertag1.subtag2']
    >>> doc2.Subjects()
    ['supertag','supertag1','supertag.subtag3','supertag1.subtag4']

and if you choose 'supertag1' as parent tag, the results list will show this:

* subtag2
* subtag4

These are links to the search page with a search parameter set to
'supertag.subtagX'.

Here you can see the keyword portlet:

.. figure:: https://github.com/redomino/redomino.advancedkeyword/raw/master/docs/resources/keywordportlet.png
   :align: center

   Keywords portlet powered by redomino.advancedkeyword (it shows a subset of existing keywords)


How to launch tests
===================
Type the following command:

::

$ ./bin/test -m redomino.advancedkeyword

Authors
=======

* Davide Moro (davidemoro) <davide.moro@redomino.com> (idea, concept, design and implementation)
* Giacomo Spettoli <giacomo.spettoli@redomino.com>
* Maurizio Lupo (sithmel) <maurizio.lupo@redomino.com>
