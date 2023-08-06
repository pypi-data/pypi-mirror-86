# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from pip._internal.req import parse_requirements
from os.path import dirname, join

import versioneer

here = dirname(__file__)

readme_file = join(here, 'README.md')

release_notes_file = join(here, 'docs', 'release_notes.rst')

requirements_file = join(here, 'requirements.txt')
requirements = parse_requirements(requirements_file, session='hack')
requirements_dev_file = join(here, 'requirements.dev.txt')
requirements_dev = parse_requirements(requirements_dev_file, session='hack')

DISTNAME              = 'stock_market'
AUTHOR                = 'kimkeatc'
AUTHOR_EMAIL          = 'kim.keat.chin@outlook.com'
MAINTAINER            = 'kimkeatc'
MAINTAINER_EMAIL      = 'kim.keat.chin@outlook.com'
DESCRIPTION           = 'A library that gather stock market historical OHLC data.'
LONG_DESCRIPTION      = open(readme_file, 'r').read() \
    + '\n\n' \
    + open(release_notes_file, 'r').read()
LONG_DESCRIPTION_TYPE = 'text/markdown'
URL                   = 'https://github.com/kimkeatc/stock-market'
DOWNLOAD_URL          = ''
PROJECT_URL           = {}

# https://pypi.org/classifiers/
CLASSIFIERS           = ['Development Status :: 1 - Planning',
                         'License :: OSI Approved :: MIT License',
                         'Operating System :: Microsoft :: Windows',
                         'Programming Language :: Python :: 3',
                         ]

DEPENDENCIES          = [ir.requirement for ir in requirements]
DEPENDENCIES_DEV      = [ir.requirement for ir in requirements_dev]

setup(
    # project info
    name=DISTNAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,

    # versioneer
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    # description
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    url=URL,
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URL,

    packages=find_packages(),
    namespace_packages=[DISTNAME],
    include_package_data = True,
    install_requires=DEPENDENCIES,
    extras_require = {'dev': DEPENDENCIES_DEV,
                      },

    classifiers=CLASSIFIERS,

    license='MIT',

    platforms='any',
    keywords='klsescreener',

    python_requires='>=3.6',
    zip_safe=False,
)
