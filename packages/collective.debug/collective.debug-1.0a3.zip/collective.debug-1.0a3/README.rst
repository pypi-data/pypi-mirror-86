.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

================
collective.debug
================

collective.debug provide a ``@@debug`` view for analyzing and debugging purposes.

Warning
--------

- Use this add-on with care because it may expose unwanted or unwanted information. 

- Use it with care for debugging and analyzing purposes only. 

- Do not use it production.


Installation
------------

Install collective.debug by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.debug


and then running ``bin/buildout``

Usage
-----

This add-on provides a ``@@debug`` browser view that returns some debugging information
on the current context object, the current user and its roles, the instance dict of the
current context object and request information.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.debug/issues
- Source Code: https://github.com/collective/collective.debug


License
-------

The project is licensed under the GPLv2.

Author
------

Andreas Jung (info@zopyx.com)
