#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


# Workaround for multiprocessing/nose issue. See http://bugs.python.org/msg170215
try:
    import multiprocessing
except ImportError:
    pass


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


# Load package meta from the pkgmeta module without loading imagekit.
pkgmeta = {}
metapath = os.path.join(os.path.dirname(__file__), 'cbsettings', 'pkgmeta.py')
exec(compile(open(metapath, 'rb').read(), metapath, 'exec'), pkgmeta)


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
        'Django>=1.8',
        'future>=0.15',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ],
    setup_requires=[],
    test_suite='nose.core.collector',
)
