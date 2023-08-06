from setuptools import setup, find_packages

setup(
    name = "QBinder",
    version = "1.0.0",
    keywords = ("pip", "PyQt","PySide", "Qt", "DataBinding","Binding","Binder"),
    description = "Global Data Binding for Python Qt framework",
    long_description = "Global Data Binding for Python Qt framework",
    license = "MIT Licence",

    url = "https://github.com/FXTD-ODYSSEY/QBinder",
    author = "timmyliang",
    author_email = "820472580@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "six~=1.15.0",
        "Qt.py~=1.3.2",
    ]
)