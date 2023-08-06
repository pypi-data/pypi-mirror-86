import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="formatlib", # Par convention, utiliser le nom du répertoire contenant votre package
    version="1.0.1",
    author="Timothée Frouté",
    author_email="timotheefroute@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://pedago-service.univ-lyon1.fr:2325/tfroute/tp_packaging",
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
