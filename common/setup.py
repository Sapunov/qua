from __future__ import unicode_literals
from setuptools import find_packages, setup


if __name__ == '__main__':
    setup(
        name='qua',
        version='0.5',

        description='QUA common library',
        long_description=None,
        url='https://github.com/Sapunov/qua',

        license='GPL3',
        author='Nikita Sapunov',
        author_email='kiton1994@gmail.com',

        platforms=['unix', 'linux', 'osx', 'windows'],

        install_requires=[],
        packages=find_packages(),
    )
