import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DownloadFromApparat", # Replace with your own username
    version="0.0.1",
    author="Abbas Niroomandi",
    author_email="46645.niroo@gmail.com",
    description="Download videos from https://www.aparat.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requiers = ["requests","re","requests_html","sys"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)