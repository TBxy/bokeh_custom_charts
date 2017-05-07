#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'numpy>=1.12',
    'pandas>=0.20',
    'bokeh>=0.12.4',
    'tornado<4.5'
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='bokeh_extended',
    version='0.0.1',
    description="Extend bokeh (http://bokeh.pydata.org) with new charts and widgets.",
    long_description=readme + '\n\n' + history,
    author="Tobias Burgherr",
    author_email='tb@wodore.com',
    url='https://github.com/TBxy/bokeh_extended',
    packages=[
        'bokeh_extended',
    ],
    package_dir={'bokeh_extended':
                 'bokeh_extended'},
    entry_points={
        'console_scripts': [
            'bokeh_extended=bokeh_extended.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='bokeh_extended',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
