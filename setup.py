#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1.0'

setup(
    name='nexmomessage',
    version=VERSION,
    description='A Python wrapper for the Nexmo API',
    author='Marco Londero',
    author_email='marco.londero@linux.it',
    license='BSD',
    url='https://github.com/marcuz/libpynexmo',
    keywords=['Nexmo', 'Python'],
    packages=['nexmomessage'],
)