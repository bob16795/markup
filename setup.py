from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="markup",
    version="0.1.0",
    keywords="example documentation tutorial",
    packages=['markup', 'markup.formaters', 'markup.data'],
    long_description=read('README.md'),
    install_requires=[
        'click',
        'pathlib',
        'python-docx',
        'pygments'
    ],
    entry_points={
        'console_scripts': ['markup = markup.cli:start']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    package_data={
        'markup': [
            'data/*'
        ],
    },
    include_package_data=True,
)
