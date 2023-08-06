import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='forsyde-io-python',
    version='0.1.2',
    author="Rodolfo Jordao",
    author_email="jordao@kth.se",
    description="ForSyDe-IO Python supporting libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rojods/forsyde-io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['networkx'],
)
