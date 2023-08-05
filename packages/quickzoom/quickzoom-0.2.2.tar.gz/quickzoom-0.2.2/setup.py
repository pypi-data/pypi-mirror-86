#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Paul Golter",
    author_email='paulgolter.de@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="quickzoom is a python command line tool that enables you easy connecting to zoom rooms",
    entry_points={
        'console_scripts': [
            'quickzoom=quickzoom.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='quickzoom',
    name='quickzoom',
    packages=find_packages(include=['quickzoom', 'quickzoom.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/paulgolter/quickzoom',
    version='0.2.2',
    zip_safe=False,
)
