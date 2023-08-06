import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sshremote",
    version="0.0.10",
    author="u1234x1234",
    author_email="u1234x1234@gmail.com",
    description=("sshremote"),
    license="MIT",
    keywords="",
    url="https://github.com/u1234x1234/sshremote",
    packages=["sshremote"],
    setup_requres=["pyngrok>=4", "pydropbear==0.0.6"],  # TODO why install_requires do not work?
    install_requires=["pyngrok>=4", "pydropbear==0.0.6"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
