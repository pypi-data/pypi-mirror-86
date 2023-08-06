import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="format-lib-package", # Replace with your own username
    version="1.0.0",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://pedago-service.univ-lyon1.fr:2325/POO/tp-packaging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
    package_dir={'': 'src'},
    python_requires='>=3.6',
)