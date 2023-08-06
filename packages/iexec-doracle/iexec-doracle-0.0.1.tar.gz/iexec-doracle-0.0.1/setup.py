import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iexec-doracle",
    version="0.0.1",
    author="iExec",
    author_email="dev@iex.ec",
    description="Tooling for build iExec doracles in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iExecBlockchainComputing/iexec-doracle-pip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
				"License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
