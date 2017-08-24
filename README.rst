=====================
Spring Platform Stats
=====================

Website to upload platform data for statistical analysis to. Used by games running on the SpringRTS engine
(https://springrts.com/).

Runs on Django / Python (https://www.djangoproject.com/) and the Django REST Framework (http://www.django-rest-framework.org/).

Development is done using Django 1.11 and Python 2.7. It may or may not run with other versions.
Latest source code can be found `on Github <https://github.com/dansan/springrts-platform-stats>`_.

License
=======

This software is licensed as GNU Affero General Public License v3 or later, see file LICENSE.

Website
=======

The live site can be found at *not yet released*.
Associated forum thread on the SpringRTS developers forum: https://springrts.com/phpbb/viewtopic.php?f=71&t=36294

Dependencies
============

See requirements.txt.

Installation
============

.. code-block:: bash

    $ virtualenv sps
    $ . sps/bin/activate
    (sps) $ pip install -U -r requirements.txt
