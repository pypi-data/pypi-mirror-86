from setuptools import setup, find_packages

setup(
    name="coolstar4",
    version="0.0.1",
    keywords=("test", "xxx"),
    license="MIT Licence",
    author="seale",
    author_email="seale@outlook.com",

    packages=find_packages(),
    install_requires=["argon2-cffi==19.2.0", "vpython"]
)
