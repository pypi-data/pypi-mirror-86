import os

from setuptools import setup


setup(
	name = 'ql-cq',
	author = 'Quantlane',
	author_email = 'code@quantlane.com',
	version = open('version.txt').read().strip(),
	url = 'https://gitlab.com/quantlane/meta/cq',
	license = 'Apache License, Version 2.0',
	long_description = open('README.md').read(),
	long_description_content_type = 'text/markdown',
	install_requires = [
		# all dependencies listed to lock the versions
		'pylint==2.6.0',
		'isort>=5.6.0,<6.0.0',
		'pyflakes-ext==2.0.0',
		'pyflakes==2.2.0',
		'ql-orange>=1.1.0,<2.0.0',
		'mypy==0.790',
		'bellybutton>=0.3.0,<0.4.0',
		'astpath[xpath]==0.6.1',
		'click>=3.0,<8.0',
		'toolz>=0.8.2,<1.0.0',
		'requirements-parser>=0.1.0',
		'pip>=19.0.0',
	],
	packages = ['cq', 'cq.checkers', 'cq.fixers'],
	package_data = {'cq': ['checkers/pylintrc', 'checkers/.bellybutton.yml']},
	entry_points = {'console_scripts': ['cq=cq.main:main']},
)
