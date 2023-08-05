import setuptools

setuptools.setup(
    name="factclient",  # Replace with your own username
    version="0.0.1",
    author="Richard Girke",
    author_email="richard.girke@campus.tu-berlin.de",
    description="Python client lib for the faas-fact library",
    url="https://github.com/faas-facts/python-fact-client",
    packages=['factclient'],
    install_requires=[
        'protobuf',
        'uuid'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
