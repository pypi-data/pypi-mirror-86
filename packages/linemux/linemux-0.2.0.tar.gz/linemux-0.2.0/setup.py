from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION") as fh:
    version = fh.read().strip()

setup(
    name='linemux',
    version=version,
    author="Rauli Kaksonen",
    author_email="rauli.kaksonen@gmail.com",
    description='File multiplexer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cincan/linemux",
    packages=['linemux'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['linemux=linemux.command:main'],
    },
    python_requires='>=3.6',
)
