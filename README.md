ABOUT QONFLUO
-------------
Qt+Confluo=Qonfluo (thing's flowing together)
Qonfluo is a streaming dashboard to stream to any sink, by now (via rtmp plugin) is capable to stream to rtmp server such as bambuser, ustream, justin.tv, youtube... Imports the fmle file that some server give to you to stream via adobe fme.

Under the hood
--------------
It uses Qt5, python3 and Gst 1.0 to do everything.  

Installation
------------
    $ git clone https://github.com/aleixq/Qonfluo.git
    $ git submodule init
    $ git submodule update
This is because there are git submodules, So when cloning you need to update these.

Needs these two libraries:

    https://github.com/jwintz/qchart.js
    https://github.com/quandyfactory/dicttoxml

To update these submodules, use:

    $ git submodule update
  
  
In Ubuntu 14.04:

    sudo apt-get  install python3-pyqt5 python3-pyqt5.qtquick 

and maybe:

    sudo apt-get install python3-gst-1.0
