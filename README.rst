pyStandardSettings
==================

Standardised settings loader

a port of nodejs `standard-settings <https://github.com/soixantecircuits/standard-settings/>`_


Why
---

No more `cp config.sample.json config.json`.

Your app presents a `settings/settings.default.json` which is always included.  
User, or other developer needing custom settings, loads his custom settings, overriding default settings.  
If a key is missing in user settings, it won't trigger any error, as a default value is in `settings.default.json`.  
`standard-settings` offers multiple ways to change settings: `settings.json` file, command line arguments, environment variables.  
Check below examples for usage and priority order.

Installation
------------

`pip install pyStandardSettings`  

Usage
-----

This module loads settings from a file, from commandline arguments, and environment variables.
It should be required at the very beginning of your project:

.. code:: python
  from pyStandardSettings import settings


Then your settings are accessible using:

.. code:: python
  print settings.server.port

Priority order
--------------

1. Environment variables

Example:

.. code:: bash
  SERVER_PORT=2500 python main.py 
  service_spacebro_inputMessage=new-media python main.py`  

2. Command line parameters (argv)

Example:  

.. code:: bash
  python main.py --server.port 2000 # to specify a field 
  python main.py --settings settings/settings.prod.json # to specify a settings file  

NB: To use a key with argv, it needs to be present in `settings.default.json`

3. Files

These files are always loaded if present:  

`settings/settings.json` first  

`settings/settings.default.json`

Working all together with different settings
--------------------------------------------

On your project, you may have other developers working with different settings.  
Pushing them in the repo is annoying. We know you've seen that before.  
Using standard-settings, developers can share common default settings, AND load custom settings.

Best practice is to add `settings/settings.default.json` in your repo, this file covers default settings, common for each developer.  
And `.gitignore` `settings/settings.json`, this file has custom settings inside. 

Schema
------

The following schema is an example of settings used in Soixante circuits apps:


.. code:: json
    {
      "server": {
          "host" : "myip",
          "port" : 3333
      },
      "timeout": {
        "lookbook": 5,
        "popup": 4
      },
      "folder": {
        "kcDownloader": "path-to/data",
        "lookbook": "path-to/lookbook"
      },
      "flag": {
        "stabalize": true,
        "devMode": true
      },
      "customKey": {
        "maxImageNumber": 64
      },
      "meta": {
          "title": "",
          "description": "",
          "message": "...",
          "source": ""
      },
      "service": {
        "altruist": {
          "host" : "192.168.1.6",
          "port" : 6666
        },
        "spacebro": {
          "host" : "192.168.1.6",
          "port" : 8888,
          "channelName": "my-channel",
          "client" : {
            "name" : "my-app"
          }
        }
      }
    }

See `soixantecircuits/standard <https://github.com/soixantecircuits/standard>`_

Goodies
-------

To list all settings keys available in your project, use


.. code:: bash
    python main.py -h


and it will display

.. code:: bash
    usage: main.py [-h] [-s SETTINGS] [--recipe RECIPE]
                   [--server.host SERVER.HOST] [--server.port SERVER.PORT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SETTINGS, --settings SETTINGS
                            settings file in json format
      --recipe RECIPE
      --server.host SERVER.HOST
      --server.port SERVER.PORT

test command
============

`python -m tests.test`
