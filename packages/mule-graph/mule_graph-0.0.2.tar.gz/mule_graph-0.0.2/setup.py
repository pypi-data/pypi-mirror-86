import setuptools

# with open('README.md', 'r') as f:
#     long_description = f.read()


setuptools.setup(
    name="mule_graph",
    version="0.0.2",
    author="levensworth",
    author_email="sbassani@mulesoft.com",
    description="small graph representation library for muleapp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.5",
)
