from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name="xbox-remote",
    version="1.0.3",
    description="A Python package to connect to xbox and interface with its buttons and joysticks",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/FRC4564/Xbox",
    author="Steven Jacobs",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["xbox"],
    include_package_data=True,
)
