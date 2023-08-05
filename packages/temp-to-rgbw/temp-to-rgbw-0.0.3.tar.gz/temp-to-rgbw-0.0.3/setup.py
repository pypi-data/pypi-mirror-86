import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()
setuptools.setup(
    name = "temp-to-rgbw",
    version = "0.0.3",
    author = "Hypercookie",
    author_email="hypercookie@gmx.de",
    description="Converts a Kelvin Temperatur to RBGW",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/TwoSolutions/TemperaturToRGBW",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requres='>3.6',
    install_requires=["numpy"]
)