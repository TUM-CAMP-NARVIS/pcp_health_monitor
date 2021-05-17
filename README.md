Installation:
=============

on Macos:
---------
   ```
   $ CFLAGS="-stdlib=libc++" pipenv install pycapnp==0.6.4
   ```

on Ubuntu 18.04
---------------
- requires python3.8
  ```
  $ sudo apt-get install python3.8 python3.8-dev python3.8-distutils
  $ sudo apt-get install --force python3-pip python3-setuptools
  $ pipenv --python 3.8 install -r requirements
  ```
  
Running:
========

for now just run main.py

```
$ pipenv shell
$ PYTHONPATH=./:$PYTHONPATH python pcp_wm/main.py
```
  
Docker
======

```
 $ docker build -t pcp-wm .
 $ docker run --rm -it pcp-wm:latest /bin/bash
 # python pcp_wm/main.py
```

Icons source:
https://freeicons.io/icon-list/e-cons-icons-set
