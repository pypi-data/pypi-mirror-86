"""
setup file to build package.

build (run from directory containing setup.py):
> python setup.py sdist bdist_wheel

Make sure wheel is installed
> sudo python -m pip install --user --upgrade setuptools wheel

upload to PyPI:
> sudo python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

"""

if __name__ == '__main__':

    import setuptools

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name='lc-data-libs',
        version='0.1.9',
        author="lc-data",
        author_email="data@gmail.com",
        description="Usefull library for lc operations",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://bitbucket.org/luckycart/lc-data",
        packages= setuptools.find_packages(include=('lcdata','lcdata.*',)),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'google-cloud-logging',
            'google-cloud-dataproc==2.0.0',
            'google-cloud-pubsub'
        ],
     )
