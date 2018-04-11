"""
Setup for gnucash_import_converter.
"""

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gnucash_import_converter',
    version='0.0.1',
    description='Convert bank statements for import in GNUCash.',
    long_description=long_description,
    url='https://github.com/silvester747/gnucash_import_from_bank',
    author='Rob van der Most',
    author_email='silvester747@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='GNUcash statements converter',
    packages=[
        'gnucash_import_converter',
    ],
    python_requires='>=3.4',
    install_requires=[],
    extras_require={
        'test': ['py.test'],
    },
    entry_points={
        'console_scripts': [
            'gnucash_import_from_bank = gnucash_import_converter.main:main',
        ],
    },
)
