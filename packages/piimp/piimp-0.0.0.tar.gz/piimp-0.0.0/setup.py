import setuptools

setuptools.setup(
    name="piimp",
    version="0.0.0",
    author="Brian C. Ferrari",
    author_email="brian.ferrari@ucf.edu",
    description="This is a Python package for post-processing ice irradiation data.",
    url="https://github.com/Cavenfish/PIIMP",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "pandas", "openpyxl", "matplotlib",
                      "xlrd", "xlsxwriter", "sklearn", "collections", "seaborn"
                      "glob"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
