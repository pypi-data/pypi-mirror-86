import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name="batch_table_storage",
    version="0.0.9",
    author="Yoeran Kaniok",
    author_email="yoeran@live.nl",
    description="Async batch functionality for Azure Table Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YoeranKaniok/batch_table_storage",
    install_requires=[
        'azure-cosmosdb-table==1.0.6'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)