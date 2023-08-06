
from setuptools import setup, find_packages

version = '0.1'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


url = 'https://github.com/pmaigutyak/mp-avtopro'


setup(
    name='django-mp-avtopro',
    version=version,
    description='Django avtopro apps',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
