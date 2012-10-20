#!/usr/bin/python
from setuptools import setup, find_packages

EXTRAS_REQUIRES = dict(
    test=[
        'fudge'
        ],
    )

for k,v in EXTRAS_REQUIRES.iteritems():
    if k == 'test':
        continue
    EXTRAS_REQUIRES['test'] += v

setup(
    name='pygeocode',
    version='0.0.3',
    description="pygeocode -- Wrapper for several public geocoding APIs",
    author='Andres Buritica, Mike Megally, Tommi Virtanen',
    author_email="andres@thelinuxkid.com, cmsimike@gmail.com, tv@eagain.net",
    maintainer="Andres Buritica",
    maintainer_email="andres@thelinuxkid.com",
    url='https://github.com/thelinuxkid/pygeocode',
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
