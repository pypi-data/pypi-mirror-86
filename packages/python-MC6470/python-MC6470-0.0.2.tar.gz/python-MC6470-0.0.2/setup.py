from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="python-MC6470",
    version="0.0.2",
    author="Mudige Tarun kumar",
    author_email="tarun.mtky@gmail.com",
    description="A python library for accessing MC6470 9-axis accelerometer from mCube via python-smbus using the I2C interface.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Vitaliz-Embedded-solutions/python-MC6470",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
