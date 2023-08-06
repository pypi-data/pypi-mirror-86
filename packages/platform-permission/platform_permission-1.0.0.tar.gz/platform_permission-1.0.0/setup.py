import os
from setuptools import setup
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(
    name='platform_permission',
    version='1.0.0',
    packages=['permissionlibrary'],
    description='Library permission',
    long_description=README,
    author='Phattara Kiantong',
    author_email='yondaimae1429@gmail.com',
    url='https://gitlab.com/the-platform1/lib_permission',
    download_url = 'https://gitlab.com/the-platform1/lib_permission/-/archive/1.0.0/lib_permission-1.0.0.tar.gz',
    license='MIT',
)
