import setuptools
from google_drive_client import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-drive-client",
    version=__version__,
    author="Sam Yao",
    author_email="turisesonia@gmail.com",
    description="Google Drive Client package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turisesonia/google_drive_client",
    packages=setuptools.find_packages(exclude=["docs", "tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
)
