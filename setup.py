"""Setup file"""
from setuptools import setup, find_packages


setup(
    name='sigfox_backend',
    version='0.1_dev',
    description='Unnoficial REST API for Sigfox Backend',
    url='https://github.com/menchopez/pythonScripts/tree/master/sigfox_backend',
    author='Menchopez',
    author_email='mmp23uc@gmail.com',
    classifiers=['Programming Language :: Python :: 2.7'],
    packages=find_packages(),
    install_requires=['requests', 'socket', 'json', 'ast', 'time', 'requests.packages.urllib3']
)


