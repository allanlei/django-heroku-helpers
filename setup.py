from distutils.core import setup
from setuptools import find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_packages_in(where, **kwargs):
    return [where] + ['%s.%s' % (where, package) for package in find_packages(where=where, **kwargs)]

setup(
    name = 'django-heroku-helpers',
    version = '0.1.0',
    author = 'Allan Lei',
    author_email = 'allanlei@helveticode.com',
    description = 'Helpers for integrating Django into Heroku',
    long_description=open('README.md').read(),
    license=open('LICENSE.txt').read(),
    keywords = 'django heroku',
    url = 'https://github.com/allanlei/django-heroku-helpers',
    packages=find_packages_in('heroku'),
    install_requires=[
    ],
)
