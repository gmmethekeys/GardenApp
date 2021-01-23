"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Project GardenApp',
    version='0.0.1',
    description='An application for garden reminders. '
                '',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TheRealMorthos/Project_GardenApp',
    author='Donald Marovich',
    author_email='dmarovic@asu.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Flask Flask-Login Users Login Authentication Tutorial',
    packages=find_packages(),  # Required
    install_requires=['flask',
                      'flask_login',
                      'flask_sqlalchemy',
                      'flask_assets',
                      'psycopg2-binary',
                      'PyMySQL',
                      'wtforms'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    entry_points={
        'console_scripts': [
            'run = __main__',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/TheRealMorthos/Project_GardenApp/issues',
        'Source': 'https://github.com/TheRealMorthos/Project_GardenApp',
    },
)
