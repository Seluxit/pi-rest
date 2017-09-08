
 RESTful Web service
===================================================

Copyright 2017 Seluxit A/S.

Intro
-----------------------
RESTful Web service is intended to work with Raspbeery Pi application [QBerry][qberry-git] for presenting GPIO states and
controlling it. It is build using [Flask][flask-org] microframework and intended to run on Raspberry or other remote
machine. It consists of two services: 

    * pipepi.py - bidirectional pipe. From application to REST service it is used to extract data and apply to REST service.     
    * restpi.py - REST service 

[qberry-git]: https://github.com/Seluxit/qberry 
[flask-org]: http://flask.pocoo.org/
[flask-uuid]: https://github.com/wbolster/flask-uuid


Requirements and installation  
-----------------------

Following libraries are needed:

  * Python 3.5 or later 
  * [Flask][flask-org] - a microframework for Python for creating RESTful Web service 
  * [Flask-UUID][flask-uuid] - UUID converter for urls on a Flask application


On Linux, you can install them with:

    $ sudo apt-get install python3 python3-pip
    $ sudo pip3 install flask Flask-UUID


## Run 

Run './pipepi.py' first and then './restpi.py'. Use systemd as init system to start services at boot.

## License

See the `LICENSE` file for details. In summary, Qplus is licensed under the
MIT license, or public domain if desired and recognized in your jurisdiction.
