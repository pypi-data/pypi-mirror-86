"""
Flask-URLSigning
----------------

A flask extension to sign and verify signed urls.
"""
from setuptools import setup

setup(
    name='Flask-URLSigning',
    version='1.0.2',
    url='https://gitlab.com/prodrigues1990/flask-urlsigning',
    license='GPLv2',
    author='Pedro Rodrigues',
    author_email='prodrigues1990@gmail.com',
    description='A flask extension to sign and verify signed urls.',
    long_description=__doc__,
    py_modules=['flask_urlsigning'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'bcrypt'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
