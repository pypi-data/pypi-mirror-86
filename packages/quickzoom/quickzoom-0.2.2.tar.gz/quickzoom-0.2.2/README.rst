=========
quickzoom
=========

quickzoom is a python command line tool that enables you easy connecting to zoom rooms


* Free software: MIT license

Features
--------
After pip install you can use the following commands in the command line

* quickzoom <roomlabel> 
    * Will search your config file for the room label. If the room label exists. Tt willl grabd the meeting id and password and connect to zoom. 
* quickzoom --newroom / -n
    * Will create a new room in your config. Will prompt you for room label, meeting id, meeting password. 

All your rooms will be saved in your homedirectory/.quickzoom/rooms.json:
    * windows: C:/Users/User/.quickzoom/rooms.json

Of course you can also manually edit the rooms.json file and quickly paste in some zoom rooms.

ToDo
--------
* implement connect.get_zoom_exe() for macOs and linux
* implement connect.connect_to_meeting() for macOs and linux

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
