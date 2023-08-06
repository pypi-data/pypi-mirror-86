import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Read __version__ in opendnn/version.py
exec(open('opendnn/version.py').read())

# This call to setup() does all the work
setuptools.setup(
    name="opendnn",
    version=__version__,
    description="opendnn",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/quanhua92/opendnn",
    author="Quan Hua",
    author_email="support@opendnn.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
