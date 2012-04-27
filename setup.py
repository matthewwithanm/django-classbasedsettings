#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name='django-classbasedsettings',
    description='Use classes to define settings.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    version='0.1.2',
    author='Matthew Tretter',
    author_email='matthew@exanimo.com',
    url='http://github.com/matthewwithanm/django-classbasedsettings',
    download_url='http://github.com/matthewwithanm/django-classbasedsettings/tarball/master',
    packages=find_packages(),
    zip_safe=False,
    keywords=['settings', 'classbased', 'class-based'],
    include_package_data=True,
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
)
