import setuptools

with open("README.md") as f:
    readmefile_contents = f.read()

setuptools.setup(
    name="lidbox",
    version="1.0.0-rc",
    description="Spoken language identification out of the box with TensorFlow",
    long_description=readmefile_contents,
    long_description_content_type="text/markdown",
    author="Matias Lindgren",
    author_email="matias.lindgren@iki.fi",
    url="https://github.com/py-lidbox/lidbox",
    license="MIT",
    python_requires=">= 3.7.*",
    install_requires=[
        "colorcet ~= 2.0.2",
        "kaldiio ~= 2.13",
        "matplotlib ~= 3.1",
        "scikit-learn ~= 0.22.2",
        "webrtcvad ~= 2.0.10",
        "miniaudio ~= 1.37",
        "pandas ~= 1.1.4",
    ],
    packages=[
        "lidbox",
        "lidbox.data",
        "lidbox.embed",
        "lidbox.features",
        "lidbox.meta",
        "lidbox.models",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
