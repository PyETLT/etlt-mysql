from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='ETLT-MySQL',

    version='0.10.0',

    description='ETLT extension for MariaDB and MySQL databases',
    # long_description=long_description,

    url='https://github.com/SetBased/py-etlt-mysql',

    author='Paul Water',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Database'
    ],

    keywords='ETLT, MySQL, MariaDB',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=['etlt', 'pytz']
)
