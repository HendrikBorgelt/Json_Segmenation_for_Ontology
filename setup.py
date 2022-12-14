#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Hendrik Borgelt",
    author_email='hendrik.borgelt@tu-dortmund.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tool for segmenting nested JSON-dictionaries and convert them into an Ontology",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='json_segmenation_for_ontology',
    name='json_segmenation_for_ontology',
    packages=find_packages(include=['json_segmenation_for_ontology', 'json_segmenation_for_ontology.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/HendrikBorgelt/json_segmenation_for_ontology',
    version='alpha.0.0',
    zip_safe=False,
)
