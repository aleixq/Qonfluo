# Licensed under the GPLv3 license

from distutils.core import setup
import glob

long_description = "Qt+Confluo=Qonfluo (thing's flowing together) Qonfluo is a streaming dashboard and video capture or webcam mixer to stream to any sink, by now (via rtmp plugin) is capable to stream to rtmp server such as bambuser or youtube... Imports the fmle file that some server give to you to stream via adobe fme. It also allow you to record."


version = '0.1'


def main():
    setup(
	  #cmdclass = {'build_py': build_py},
          name='qonfluo',
          version=version,
          description='Streaming videomixer',
          long_description=long_description,
          author='Aleix Quintana',
          author_email='kinta@communia.org',
          url='http://communia.org/content/projecte/qonfluo',
          download_url='https://github.com/aleixq/Qonfluo',
          license='GPL',
          maintainer='Aleix Quintana Alsius',
          maintainer_email='kinta@communia.org',
          platforms='any',
          keywords=['Streaming', 'Videomixer', 'v4l2 mixer','Record'],
          scripts=['qonfluo.py'],
          packages=['qonfluo',
                    'qonfluo/dicttoxml',
                   ],
          #install_requires = ['dicttoxml'], # by now adding dicttoxml with no need to install requires
          data_files=[
              ('share/applications',['qonfluo.desktop']),
              ('share/pixmaps', ['qonfluo.svg']),
              ('share/libqonfluo/qml', glob.glob('qml/*')),
              ('share/libqonfluo/qml/jBQuick',glob.glob('qml/jbQuick/*')),
              ('share/libqonfluo/qml/jBQuick/Charts', glob.glob('qml/jbQuick/Charts/*')),
              ('share/libqonfluo/images', glob.glob('images/*.*')), 
              ('share/doc/qonfluo',['README.md']),              
              ],
          classifiers=['Development Status :: 4 - Beta',
                       'Environment :: Other Environment',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GPLv3 License',
                       'Natural Language :: English',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: Python',
                       'Topic :: Multimedia :: Video :: Capture',
                       'Topic :: Multimedia :: Video',
                       'Topic :: Multimedia'])


if __name__ == '__main__':
    main()

