from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='linkedin profile picture',  
    version='0.0.1',
    author="Shashank Deshpande",
    author_email="shashankdeshpande18@gmail.com",
    description="Python package to crawl linkedin profile pictures using google custom search API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shashankdeshpande/linkedin",
    python_requires=">=3.6.0",
    packages=find_packages()
    )
