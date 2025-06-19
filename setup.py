from setuptools import setup, find_packages

setup(
    name="classmap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "astroid==3.0.3",
        "graphviz==0.20.1",
    ],
    entry_points={
        'console_scripts': [
            'classmap=classmap.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Python Class Inheritance Analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
) 