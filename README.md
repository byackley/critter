The Critter Engine is an engine for 2D game development, meant for a roughly
8-to-16-bit feel. In other words, it's "12-bit", which is where the name
Studio Dodec comes from. It uses Pygame as a basis, but abstracts and
simplifies away a lot of the details.


PYTHON AND PYTHON VIRTUALENV INSTALLATION
Python virtualenv is strongly recommended. Many OSes will not have Python 2.x
installed by default, so that will also need to be done.

OS X
Critter Engine assumes a reasonably complete Python environment.
For 'a reasonably complete Python environment' in OS X, see
http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-mac-os-x/

Instructions provided will walk you through installing brew, Xcode, Command
Line Tools for Xcode, and finally, python itself.
Once python is installed, update your basic library set with the following:
pip2 install -U pip setuptools
pip2 install virtualenv

Linux
TBD
Windows
TBD


LIBRARY INSTALLATION (assuming virtualenv)
Once you have python and virtualenv installed, you can set up your virtualenv.

git clone https://github.com/byackley/critter.git
cd critter
virtualenv ve
source ve/bin/activate
pip install -U pip setuptools
pip install -U -r requirements.txt


ENGINE EXECUTION (example)
python ceStage.py


Have fun!
