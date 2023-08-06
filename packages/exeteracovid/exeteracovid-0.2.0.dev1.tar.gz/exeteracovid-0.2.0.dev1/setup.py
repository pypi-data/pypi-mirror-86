from setuptools import setup

from exeteracovid import __version__

setup(
    name='exeteracovid',
    version=__version__,
    description='Analytics for the Covid Symptom Study, based on ExeTera',
    url='https://github.com/kcl-bmeis/ExeTeraCovid',
    author='Ben Murray',
    author_email='benjamin.murray@kcl.ac.uk',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    packages=['exeteracovid', 'exeteracovid.algorithms', 'exeteracovid.processing'],
    install_requires=[
        'exetera>=0.4'
    ]
)
