from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Fredy Somy",
    author_email="fredysomy@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="A python library to scrape github",
    install_requires=['fire','beautifultable','random'],
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    
    version="0.1.5",
    keywords="pysondb,database,json",
    name="pysondb",
    packages=find_packages(),
    entry_points={
        'console_scripts':[
        'pysondb=pysondb.cli:main']
    },
    setup_requires=[],
    url="https://github.com/fredysomy/pysonDB",
  
    zip_safe=False,
)
