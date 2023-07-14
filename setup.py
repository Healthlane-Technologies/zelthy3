from setuptools import setup, find_packages

setup(
    name='zelthy3',
    version='0.1',
    description='Zelthy3 AppDev Framework',
    author='Zelthy ("Healthlane Technologies")',
    author_email='platform@zelthy.com',
    url='https://github.com/Healthlane-Technologies/zelthy3',
    packages=find_packages(),
    install_requires=[
        'django>=3.0',
        "psycopg2-binary",
        'django-tenants',
        'djangorestframework',
        'django-rest-knox'

        # Other dependencies...
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        # Other classifiers...
    ],
    entry_points={
        'console_scripts': [
            'zelthy3=zelthy3.cli:main',
        ],
    },
)
