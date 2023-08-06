"""Сценарий установки"""


from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='BinarySearchProgram',
    version='1.0.1',
    description='Binary search program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pavel Artemyev',
    author_email='sanchello13pv@gmail.com',
    packages=find_packages(),
    package_dir={'': 'package'},
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
                 'run=package:__main__',
        ],
    },

)
