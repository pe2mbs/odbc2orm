#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.dist import Distribution


class BinaryDistribution( Distribution ):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules( foo ):
        return True

    def is_pure( self ):
        return True


setup(  name                = 'odbc2orm',
        version             = '1.0.5',
        description         = 'Convert ODBC schema to ORM',
        long_description    = open("README.md","r" ).read(),
        long_description_content_type = 'text/markdown',
        author              = 'Marc Bertens-Nguyen',
        author_email        = 'm.bertens@pe2mbs.nl',
        url                 = 'https://github.com/pe2mbs/odbc2orm',
        install_requires    = [ 'PyYAML',
                                'pyodbc',
                                'Mako'],
        classifiers         = [ 'Environment :: Console',
                                'Operating System :: Microsoft :: Windows',
                                'Intended Audience :: Developers',
                                "License :: OSI Approved :: GNU General Public License (GPL)",
                                'Programming Language :: Python :: 3', ],
        distclass           = BinaryDistribution,
        keywords            = 'odbc sqlalchemu orm',
        packages            = find_packages( exclude = [ 'custom',
                                                     'template' ] ),
        python_requires     = '>3',
        entry_points        = {  # Optional
            'console_scripts': [
                'odbc2orm=odbc2orm.__main__:main',
            ],
        },
        project_urls        = {  # Optional
            'Source Public':    'https://github.com/pe2mbs/odbc2orm/',
            'Bug Reports':      'https://github.com/pe2mbs/odbc2orm/issues',
            'Say Thanks!':      'https://github.com/pe2mbs/odbc2orm/saythanks',
        },
)