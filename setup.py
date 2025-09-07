#!/usr/bin/env python3
"""
Setup configuration for Legal Memespace package.

This package implements evolutionary analysis of legal systems using
the Extended Phenotype Theory applied to comparative law research.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Filter out comments and empty lines
requirements = [req for req in requirements if req and not req.startswith('#')]

setup(
    name='legal-memespace',
    version='0.1.0',
    author='Ignacio Adrián Lerer',
    author_email='ignacio.lerer@example.com',  # Replace with actual email
    description='Framework for evolutionary analysis of legal systems using Extended Phenotype Theory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ialerer/legal-memespace',
    project_urls={
        'Bug Tracker': 'https://github.com/ialerer/legal-memespace/issues',
        'Documentation': 'https://legal-memespace.readthedocs.io/',
        'SSRN Papers': 'https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=XXXXX',  # Replace with actual SSRN ID
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Sociology :: History',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.910',
            'pre-commit>=2.15.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
            'nbsphinx>=0.8.0',
        ],
        'all': [
            'pytest>=6.2.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.910',
            'pre-commit>=2.15.0',
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
            'nbsphinx>=0.8.0',
        ]
    },
    keywords=[
        'legal theory',
        'evolution',
        'memetics',
        'comparative law',
        'extended phenotype',
        'anti-corruption',
        'legal evolution',
        'evolutionary biology',
        'jurisprudence',
        'legal systems'
    ],
    entry_points={
        'console_scripts': [
            'legal-memespace=legal_memespace.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'legal_memespace': ['data/*.json', 'data/*.yaml'],
    },
    zip_safe=False,
)