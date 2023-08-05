from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='bc125at-perl-helper',
	version='1.2.2',
	packages=['bc125at_perl_helper'],
	url='https://github.com/itsmaxymoo/BC125AT-Perl-Helper',
	license='MIT License',
	author='Max Loiacono',
	author_email='',
	description='A tool to convert bc125at-perl\'s output to CSV and back.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	entry_points={
		'console_scripts': ['bc125at-perl-helper=bc125at_perl_helper:main']
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6'
)
