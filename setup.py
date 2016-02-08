import os
from setuptools import setup, find_packages


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

version = {}
with open(os.path.join(os.path.dirname(__file__),
                       'flask_swag', 'version.py')) as f:
    exec(f.read(), version)


setup(
    name='Flask-Swag',
    version=version['VERSION'],
    description='Build swagger spec with Flask.',
    long_description=readme(),
    license="MIT License",
    author='Choi Geonu',
    author_email='6566gun@gmail.com',
    url='https://github.com/hardtack/flask-swag',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Flask >= 0.9',
        'marshmallow >= 2.5.0',
    ],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
