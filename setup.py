#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


# Load package meta from the pkgmeta module without loading imagekit.
pkgmeta = {}
execfile(os.path.join(os.path.dirname(__file__),
         'cbsettings', 'pkgmeta.py'), pkgmeta)


setup(
    name='django-classbasedsettings',
    description='Use classes to define settings.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    version=pkgmeta['__version__'],
    author=pkgmeta['__author__'],
    author_email='m@tthewwithanm.com',
    url='http://github.com/matthewwithanm/django-classbasedsettings',
    download_url='http://github.com/matthewwithanm/django-classbasedsettings/tarball/master',
    packages=find_packages(),
    zip_safe=False,
    keywords=['settings', 'classbased', 'class-based'],
    include_package_data=True,
    tests_require=[
        'nose',
        'unittest2',
    ],
    install_requires=[
        'Django>=1.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    setup_requires=[],
    test_suite='runtests.collector',
)
