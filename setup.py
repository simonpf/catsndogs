from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='catsndogs',  # Required
    version='0.0.4',  # Required
    description='A dataset containing cats and dogs.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/simonpf/catsndogs',  # Optional
    author='Simon Pfreundschuh',  # Optional
    author_email='simon.pfreundschuh@chalmers.se',  # Optional
    install_requires=["appdirs", "requests"],
    packages=["catsndogs"],
    python_requires='>=3.6',
    project_urls={  # Optional
        'Source': 'https://github.com/simonpf/catsndogs/',
    })
