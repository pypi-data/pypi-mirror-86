from setuptools import find_packages, setup
setup(
    name="ls-orb",
    packages=find_packages(include=["orb"]),
    version="0.1.0",
    description="Livspace Orb core library",
    author="vivek.paidi@livspace.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Django==2.2.6',
        'djangorestframework==3.10.3',
        'django-filter==2.2.0',
        'newrelic==5.6.0.135',
        'jsonschema==3.1.1',
        'drf-yasg==1.17.1',
        'django-cors-headers==3.1.1',
        'pylint==2.4.3',
        'pylint-django==2.0.13',
        'google-api-python-client==1.8.0',
        'google-auth-httplib2==0.0.3',
        'google-auth-oauthlib==0.4.1',
    ]
)
