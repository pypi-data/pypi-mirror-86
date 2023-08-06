#!/usr/bin/env python

import setuptools

long_description = """

"""


setuptools.setup(
    name='colour-stacking',
    version='0.1',
    description='Optimisation of coloured line thickness when displaying maps',
    # long_description=long_description,
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
        "z3-solver",
        "pydantic",
        "shapely",
    ]
)
