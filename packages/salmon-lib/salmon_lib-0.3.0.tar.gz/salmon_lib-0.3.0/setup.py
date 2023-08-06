from setuptools import setup

setup(
    name="salmon_lib",
    version="0.3.0",
    description="a library to read and write CRiSP harvest files",
    url="https://github.com/Society-for-Internet-Blaseball-Research/salmon_lib",
    author="alisww",
    author_email="waylandalis@gmail.com",
    license="MIT",
    packages=["salmon_lib", "salmon_lib.parsers", "salmon_lib.resources"],
    install_requires=["matplotlib==3.3.3"],
    include_package_data=True,
    zip_safe=False,
)
