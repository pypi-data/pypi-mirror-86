import setuptools

with open('README.md','r') as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'betterNeural',
	version = '0.0.5',
	author = 'riioze',
	author_email = 'riioze0@gmail.com',
	description = 'A package with tools for Neural networks',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/riioze/betterneural',
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"],
	python_requires = '>=3.6',
	install_requires=['numpy'])