from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

with open('README.md') as inp:
    readme_content = inp.read()

setup(
    name = 'ioweb',
    version = '0.0.29',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    maintainer='Gregory Petukhov',
    maintainer_email='lorien@lorien.name',
    url='https://github.com/lorien/ioweb',
    description = 'Web Scraping Framework',
    long_description = readme_content,
    long_description_content_type='text/markdown',
    packages = find_packages(exclude=['test', 'crawlers']),
    download_url='https://github.com/lorien/ioweb/releases',
    license = "MIT",
    entry_points = {
        'console_scripts': [
            'ioweb=ioweb.cli:command_ioweb',
            'gioweb=ioweb_gevent.cli:command_ioweb',
        ],
    },
    install_requires = [
        'urllib3<=1.25.6',
        'pyopenssl',
        'cryptography',
        'idna',
        'certifi',
        'cachetools',
        'gevent',
        'pysocks',
        'lxml',
        'defusedxml',
        'selection',
        'cssselect',
        'python-json-logger',
        'psutil',
        'defusedxml',
        'pymongo', # it is required for "bson" package, FIXME: REMOVE
    ],
    keywords='web scraping network crawling cralwer spider pycurl',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
