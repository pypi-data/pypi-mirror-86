from setuptools import setup, find_packages
import pathlib

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='catastro-finder',
    version='1.2.0', 
    description='Unofficial Catastro Finder. No API keys required', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[''],
    url='https://github.com/jorgeramirezcarrasco/catastro-finder',  
    author='Jorge Ramírez Carrasco',
    keywords='catastro, web scraping',
    python_requires='>=3.6, <4',
    install_requires=[
                    'beautifulsoup4>=4.9.3',
                    'certifi>=2020.11.8',
                    'chardet>=3.0.4',
                    'idna>=2.10',
                    'requests>=2.25.0',
                    'soupsieve>=2.0.1',
                    'urllib3>=1.26.2'
                    ]
)