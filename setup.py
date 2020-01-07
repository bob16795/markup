from setuptools import setup
import os


setup(
    name="markup",
    version="0.1.0",
    keywords="markdown compiler python script",
    packages=['markup', 'pdfer'],
    install_requires=[
        'click',
        'pathlib',
        'pygments',
        'Pillow'
    ],
    entry_points={
        'console_scripts': ['markup = markup.cli:start',
                            'mu = markup.cli:start']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
