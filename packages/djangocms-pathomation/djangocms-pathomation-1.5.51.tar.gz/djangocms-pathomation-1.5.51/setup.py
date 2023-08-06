from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='djangocms-pathomation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.5.51',
    author='Pathomation',
    author_email='info@pathomation.com',
    packages=find_packages(),
    install_requires=[
        'pma-python',
     
    ]
)



