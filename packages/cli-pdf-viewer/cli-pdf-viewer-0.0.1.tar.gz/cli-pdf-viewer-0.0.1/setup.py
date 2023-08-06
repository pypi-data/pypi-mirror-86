import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cli-pdf-viewer",
    version="0.0.1",
    author="Tabacaru Eric",
    author_email="erick.8bld@gmail.com",
    description="PDF Viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['pdfviewer'],
    packages=setuptools.find_packages(),
    scripts=[
        os.path.abspath(os.path.join("src", "pdfviewer.py"))
    ],
    install_requires=[
        'pdf2image',
        'pillow',
        'Click'
    ],
    entry_points='''
        [console_scripts]
        pdf=pdfviewer:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
