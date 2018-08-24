from distutils.core import setup
from cmdb import __title__, __version__, __license__, __author__
setup(
    name=__title__,
    version=__version__,
    packages=['cmdb'],
    license=__license__,
    long_description=open('README.md').read(),
    author=__author__
)
