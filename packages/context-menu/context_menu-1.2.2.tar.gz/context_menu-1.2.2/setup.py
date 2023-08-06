import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="context_menu",
    version="1.2.2",
    description="Library to create cross-platform native context menus.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/saleguas/context_menu",
    author="Salvador Aleguas",
    author_email="salvador@aleguas.dev",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=setuptools.find_packages(),
)
