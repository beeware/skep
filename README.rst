** NOTE: This service was used by Briefcase v0.3.0 - v0.3.9. However, in Briefcase
v0.3.10, templates locked their preferred support package. This service will be
retained for support of legacy Briefcase versions, but the behavior is now "static",
returning the support pacakges that were current as of the release of v0.3.10. Once
traffic has dropped off, this service will be retired.**

Skep
====

.. image:: https://github.com/beeware/skep/workflows/CI/badge.svg
   :target: https://github.com/beeware/skep/actions
   :alt: Build Status

.. image:: https://img.shields.io/discord/836455665257021440?label=Discord%20Chat&logo=discord&style=plastic
   :target: https://beeware.org/bee/chat/
   :alt: Discord server

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

To run the skep test suite, your currently active AWS credentials must have
access to S3 APIs. You may need to add an `AWS_PROFILE` definition to your
environment::

    $ AWS_PROFILE=beeware pytest

Deploying
---------

Deploying to the official repositories requires a developer login on the
BeeWare AWS account. You need API credentials named ``beeware`` configured.

To update the development deployment (https://dev.briefcase-support.org)::

    $ zappa update dev

To update the production deployment (https://briefcase-support.org)::

    $ zappa update prod


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
