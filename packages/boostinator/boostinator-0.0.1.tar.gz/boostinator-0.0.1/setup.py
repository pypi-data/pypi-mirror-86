'''Manage boost dependencies for python c/c++ extensions.'''

import pathlib
from distutils.core import setup
from setuptools import find_packages

from boostinator import get_include_dir


# download boost for release so we don't have to put it
# under version control; only meant to be run before
# uploading to pypi!
BOOST_DIR = get_include_dir() / 'boost'
if not BOOST_DIR.exists():
    from tempfile import TemporaryDirectory
    from shutil import copytree
    from urllib.request import urlopen
    from zipfile import ZipFile
    URL = 'https://dl.bintray.com/boostorg/release/1.74.0/source/boost_1_74_0.zip'
    with TemporaryDirectory() as tmpdir:
    # tmpdir = str(pathlib.Path('tmp').resolve())
        tmpdirp = pathlib.Path(tmpdir)
        tmpzip = tmpdirp / 'tmp.zip'
        with open(tmpzip, 'wb') as fp:
            fp.write(urlopen(URL).read())
            fp.flush()
            ZipFile(tmpzip).extractall(path=tmpdir)
            SRC = str(tmpdirp / 'boost_1_74_0/boost')
            DEST = str(get_include_dir() / 'boost')
            copytree(SRC, DEST)


setup(
    name='boostinator',
    version='0.0.1',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/boostinator',
    license='MIT',
    description='Make Boost C++ libraries available for building Python C/C++ extensions',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt', encoding='utf-8').read().split(),
    python_requires='>=3.6',
)
