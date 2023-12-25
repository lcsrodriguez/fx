import setuptools
from fxdata import (__version__,
                    __author__,
                    __package_name__)

with open("README.md", "r") as f:
    long_description = f.read()

PYTHON_MODULE_NAME: str = __package_name__
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setuptools.setup(
    name=PYTHON_MODULE_NAME,
    py_modules=[PYTHON_MODULE_NAME],
    version=__version__,
    author=__author__,
    author_email="lcsrodriguez@pm.me",
    license="MIT",
    maintainer=__author__,
    maintainer_email="lcsrodriguez@pm.me",
    url="https://github.com/lcsrodriguez/fx",
    description="FX high-frequency tick/candle historical data scraping tool",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': '.'},
    extras_require={
        "interactive": ["notebook==7.0.6"],
    },
    install_requires=REQUIREMENTS,  # [],
    python_requires='>=3.10',
    keywords=["python", "FX prices", "fx", "tick data"],
)
