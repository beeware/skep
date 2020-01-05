Skep
====

.. image:: https://github.com/beeware/skep/workflows/CI/badge.svg
   :target: https://github.com/beeware/skep/actions
   :alt: Build Status

.. image:: https://badges.gitter.im/beeware/general.svg
   :target: https://gitter.im/beeware/general
   :alt: Chat on Gitter

Skep is a lightweight proxy for serving `Briefcase
<https://github.com/beeware/briefcase>`__ support files.

It is a Flask app, deployed in production as
`briefcase-support.org <https://briefcase-support.org>`__.

Getting started
---------------

To set up and run Skep locally, create a virtual environment, install the
requirements, and run the app::

    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements/dev.txt
    (venv) $ FLASK_ENV=development FLASK_APP=skep.skep flask run

This will start a server at `http://127.0.0.1:5000/
<http://127.0.0.1:5000/>`__.

Running tests
-------------

To run the skep test suite::

    $ pytest

Deploying
---------

To update the development deployment::

    $ zappa update dev

Colophon
--------

A `Skep <https://en.wikipedia.org/wiki/Beehive#Skeps>`__ is a woven straw or
wicker basket used as a beehive.

Community
---------

Skep is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `beeware/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

If you experience problems with Skep, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://beeware.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _beeware/general: https://gitter.im/beeware/general
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/
.. _log them on Github: https://github.com/beeware/skep/issues
.. _fork the code: https://github.com/beeware/skep
.. _submit a pull request: https://github.com/beeware/skep/pulls
