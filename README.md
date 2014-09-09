ABOUT QONFLUO
-------------
Qt+Confluo=Qonfluo (thing's flowing together)
Qonfluo is a streaming dashboard to stream to any sink, by now (via rtmp plugin) is capable to stream to rtmp server such as bambuser, ustream, justin.tv, youtube... Imports the fmle file that some server give to you to stream via adobe fme.

Under the hood
--------------
It uses Qt5, python3 and Gst 1.0 to do everything.  

Getting, Running, Packaging and Installing
-------------------------
##Getting

    $ git clone https://github.com/aleixq/Qonfluo.git
    $ git submodule init
    $ git submodule update

This is because there are git submodules, So when cloning you need to update these.

Needs these two libraries:

    https://github.com/jwintz/qchart.js
    https://github.com/quandyfactory/dicttoxml

To update these submodules, use:

    $ git submodule update  
 
##Dependencies

Ubuntu 14.04:

    $ sudo apt-get  install python3-pyqt5 python3-pyqt5.qtquick python3-gst-1.0 python3-gi gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-plugins-libav
 
##Running (no install)

After getting source and dependencies you can run from command line with just " ./qonfluo-run  ".

##Packaging and Installing (pip way)

If you want to package it, we have setup.py from distutils to be done easily. However pip doesn't deal with the above dependencies, so you'll need to install before running qonfluo

to package run:

    $ python setup.py sdist

after that:

    $ cd dist
    $ sudo pip install qonfluo*.tar.gz 

this will install and then you can run qonfluo wherever you choose (qonfluo-run from cli, or searching Qonfluo in video section in freedesktops). 
( to uninstall:  pip uninstall qonfluo )

##Packaging and Installing (debian way)
This way will deal with all dependencies and will get everything just installed.
for Ubuntu (hope for Debian too but not tested), calling 

    $ python3 setup.py --command-packages=stdeb.command bdist_deb
    or
    $ python setup.py --command-packages=stdeb.command  sdist_dsc --with-python2=False --with-python3=True  bdist_deb

will add a 'one-click' installable deb package in directory dist_deb (the file ending with .deb)

