from setuptools import setup, find_packages

setup(
    name='Flask-Swag',
    version='0.1.0',
    description='Build swagger spec with Flask.',
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
