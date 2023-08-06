from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="parking-lot",
    version="1.0.3",
    description="A Python package to which allocate parking slot for Car.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Shubham Gupta",
    author_email="gshubham934@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["parking_lot"],
    include_package_data=True,
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "parking-lot = parking_lot.index:main",
        ]
    },
)
