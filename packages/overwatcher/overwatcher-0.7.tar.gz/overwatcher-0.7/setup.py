import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='overwatcher',
    version='0.7',
    author="zeionara",
    author_email="zeionara@gmail.com",
    description="A simple app for sending telegram notification on completion of a long-running command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeionara/overwatcher",
    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'python-telegram-bot'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
