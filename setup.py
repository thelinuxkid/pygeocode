#!/usr/bin/python
from setuptools import setup, find_packages
import os

EXTRAS_REQUIRES = dict(
    test=[
        'fudge>=1.0.3',
        'nose>=1.1.2',
        ],
    )

for k,v in EXTRAS_REQUIRES.iteritems():
    if k == 'test':
        continue
    EXTRAS_REQUIRES['test'] += v

# Pypi package documentation
root = os.path.dirname(__file__)
path = os.path.join(root, 'README.rst')
with open(path) as fp:
    long_description = fp.read()

setup(
    name='pygeocode',
    version='0.0.5',
    description="pygeocode -- Wrapper for several public geocoding APIs",
    long_description=long_description,
    author='Andres Buritica, Mike Megally, Tommi Virtanen',
    author_email="andres@thelinuxkid.com, cmsimike@gmail.com, tv@eagain.net",
    maintainer="Andres Buritica",
    maintainer_email="andres@thelinuxkid.com",
    url='https://github.com/thelinuxkid/pygeocode',
    license='MIT',
    packages = find_packages(),
    namespace_packages = ['pygeocode'],
    test_suite='nose.collector',
    install_requires=[
        'setuptools',
        ],
    extras_require=EXTRAS_REQUIRES,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
)
