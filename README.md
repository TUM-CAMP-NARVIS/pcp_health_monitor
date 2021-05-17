Installation:
=============

on Ubuntu 18.04
---------------
- requires python3.8
  ```
  $ sudo apt-get install python3.8 python3.8-dev python3.8-distutils
  $ sudo apt-get install --force python3-pip python3-setuptools
  $ pip install -r requirements.txt
  ```
  
Running:
========

for now just run main.py

```
$ PYTHONPATH=./:$PYTHONPATH python health_monitor --config ./resources/config/debug.yml
```
  
Docker
======

```
 $ docker build -t health_monitor .
 $ docker run --rm health_monitor:latest
```

Icons source:
https://freeicons.io/icon-list/e-cons-icons-set
