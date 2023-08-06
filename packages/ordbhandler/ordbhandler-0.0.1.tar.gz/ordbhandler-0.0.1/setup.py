import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ordbhandler",
    version="0.0.1",
    author="Leonardo de Araújo",
    author_email="dearaujo@uni-bremen.de",
    description="RDMS Data Management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardomra/ordbhandler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["mysql-connector-python==8.0.21"],
)