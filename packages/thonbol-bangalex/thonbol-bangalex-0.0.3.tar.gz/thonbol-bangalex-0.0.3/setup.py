import os
import setuptools

VERSION = open(os.path.join("thonbol", "_version.py")).\
    readlines()[0].strip(' "\n')

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
        name="thonbol-bangalex",
        version=VERSION,
        author="Bang Alex",
        author_email="bangalex.bee@gmail.com",
        description="Thonbol for data bol (Fake Data)",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/thonbol-bangalex/",
        download_url=("https://pypi.python.org/packages/source/m/thonbol-bangalex/"+"thonbol-bangalex-%s.tar.gz" % VERSION),
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6'
)
