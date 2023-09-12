from setuptools import setup, find_packages

# Super variables
VERSION = "1.0.0"
DESCRIPTION = "fx - FX tick/candle data collector"

# Description
with open(file="README.md", mode="r") as f:
    LONG_DESCRIPTION: str = f.read()
print(LONG_DESCRIPTION)

# Setting up the package
setup(
    # the name must match the folder name 'verysimplemodule'
    name="fx",
    version=VERSION,
    author="Lucas RODRIGUEZ",
    author_email="<>",
    maintainer="Lucas RODRIGUEZ",
    maintainer_email="<>",
    url="https://github.com/lcsrodriguez/fx",
    license="MIT License",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # Add any additional packages that needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "FX prices", "fx"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)