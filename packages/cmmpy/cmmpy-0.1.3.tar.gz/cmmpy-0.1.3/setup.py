import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmmpy",
    version="0.1.3",
    author="Alessandro Comunian",
    author_email="alessandro.comunian@unimi.it",
    description="Implementation of the Comparison Model Method",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://bitbucket.org/alecomunian/cmmpy",
    packages=['cmmpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
    ],
    keywords = "hydrogelogy, modelling, inverse problem, direct inverse problem, modflow, flopy",
    project_urls = {
        'Documentation': 'https://cmmpy.readthedocs.io/en/latest/index.html',
        'Source': 'https://bitbucket.org/alecomunian/cmmpy',
        },
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "flopy",
        "gstools",
        ],
    py_modules = ["tools", "cmm"],
    package_dir = {"": "."}
)
