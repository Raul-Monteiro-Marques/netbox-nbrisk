import codecs
import os.path

from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox-nbrisk',
    version=get_version('nb_risk/version.py'),
    description='NIST 800-30 Risk Management for Netbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Raul-Monteiro-Marques/netbox-nbrisk',
    author='Renato Almeida Oliveira, Raul Monteiro Marques',
    author_email='renato.almeida.oliveira@gmail.com',
    install_requires=[
        'packaging',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'nb_risk': [
            'templates/*',
            'migrations/*',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'netbox_plugins': [
            'nb_risk=nb_risk:NbriskConfig',
        ],
    },
)
