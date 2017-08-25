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

The live site can be found at *not yet released*. A test installation is at http://stats.replays.springrts.com/ .
Associated forum thread on the SpringRTS developers forum: https://springrts.com/phpbb/viewtopic.php?f=71&t=36294

Dependencies
============

See requirements.txt.

Installation
============

.. code-block:: bash

    git clone https://github.com/dansan/springrts-platform-stats.git
    mkdir springrts-platform-stats/logs
    $ virtualenv sps
    $ . sps/bin/activate
    (sps) $ pip install -U -r springrts-platform-stats/requirements.txt
    (sps) $ ./manage.py migrate
    (sps) $ ./manage.py createsuperuser
    (sps) $ sps/bin/python sps/bin/gunicorn --log-syslog --capture-output --reload --timeout 60 --name sps --bind 127.0.0.1:8999 springrts_platform_stats.wsgi


* Login into the Django admin page with the superuser account.
* Create a group "machine-creators" and give it permissions to `api|machine|Can add machine` and `api|machine|Can change
machine`.
* To allow users to post to API, add them to that group.

Python Client API
=================

http://www.django-rest-framework.org/topics/api-clients/#python-client-library

TL;DR:

.. code-block:: python

    import coreapi
    client = coreapi.Client(auth=('user', 'password'))
    schema = client.get('https://stats.replays.springrts.com/')
    action = ['machine', 'create']
    params = {
        'accountId': 12345,
        'cpuName': 'Intel i7-7700K CPU @ 4.0GHz',
        'osFamily': 'Linux',
        'platformData': {
            'ram': 1024,
            'glslVersion': '4.50 NVIDIA',
            'glSupport24bitDepthBuffer': True,
            'gpu': 'GeForce GTX 760/PCIe/SSE2',
            'new1': 'stuff1',
            'new2': 'stuff2',
        },
    }
    result = client.action(schema, action, params=params)
    # result is an OrderedDict

JavaScript Client API
=====================

http://www.django-rest-framework.org/topics/api-clients/#javascript-client-library

TL;DR:

.. code-block:: javascript

    <script src="http://stats.replays.springrts.com/static/rest_framework/js/coreapi-0.1.0.js"></script>
    <script src="http://stats.replays.springrts.com/docs/schema.js"></script>

    var coreapi = window.coreapi  // Loaded by `coreapi.js`
    var schema = window.schema    // Loaded by `schema.js`

    // Authentication
    var auth = coreapi.auth.BasicAuthentication({
        username: '<username>',
        password: '<password>'
    })
    // Initialize a client
    var client = new coreapi.Client({auth: auth})

    // Interact with the API endpoint
    var action = ["machine", "create"]
    var params = {
        accountId: ...,
        cpuName: ...,
        osFamily: ...,
        platformData: ...,
    }
    client.action(schema, action, params).then(function(result) {
        // Return value is in 'result'
    })
