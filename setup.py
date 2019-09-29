import os
from setuptools import find_packages, setup
from django_admob_ssv import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-admob-ssv',
	version=__version__,
	packages=find_packages(),
	include_package_data=True,
	license='MIT License',
    description='Admob Server-Side Verification for Django projects',
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/DoctorJohn/django-admob-ssv',
	author='Jonathan Ehwald',
	author_email='pypi@ehwald.info',
    install_requires=[
		'Django>=1.11',
        'ecdsa>=0.13.2',
	],
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 1.11',
		'Framework :: Django :: 2.0',
		'Framework :: Django :: 2.1',
		'Framework :: Django :: 2.2',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Internet :: WWW/HTTP',
	],
)
