import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aptwe',
    version='0.1.1',
    author='Philipp Hülsdunk',
    author_email='mail@huelsdunk.tech',
    description='Parser framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/phuelsdunk/aptwe',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
