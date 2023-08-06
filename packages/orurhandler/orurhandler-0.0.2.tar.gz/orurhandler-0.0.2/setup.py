import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orurhandler",
    version="0.0.2",
    author="Leonardo de Araújo",
    author_email="dearaujo@uni-bremen.de",
    description="User Management with AWS Cognito.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardomra/orurhandler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["boto3==1.14.25"],
)