#!/usr/bin/env python

import setuptools

long_description = """
Optimisation of coloured line thickness when displaying maps',
"""


setuptools.setup(
    name='colour-stacking',
    version='0.3',
    description='Optimisation of coloured line thickness when displaying maps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='JB Robertson',
    author_email='jbr@freeshell.org',
    url='https://www.gitlab.com/jbrobertson/colour-stacking',
    packages=['colour_stacking'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "z3-solver==4.8.9.0",
        "pydantic==1.7.2",
        "shapely==1.7.1",
    ]
)
