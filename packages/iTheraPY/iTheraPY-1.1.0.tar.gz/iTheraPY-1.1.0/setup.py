import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# This is not recommended, but in our case we want concrete dependencies
# to be installed upon "pip install iTheraPY" given that this is only
# meant to replicate dev environment and ensure the functionning of iThera
# tools
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="iTheraPY",
    version="1.1.0",
    author="ilib",
    author_email="ilib@ithera-medical.com",
    description="Environment for iThera Python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.8',
)
