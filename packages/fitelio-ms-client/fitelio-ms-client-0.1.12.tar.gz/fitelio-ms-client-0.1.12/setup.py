from setuptools import find_packages, setup

from fms import __version__ as version

requirements = ["grpcio", "grpcio-tools", "requests", "typing-extensions", "protobuf", "structlog",
                "grpcio-health-checking"]

extras_require = {
    "test": ["pytest-cov", "pytest-django", "pytest"],
    "lint": ["flake8", "wemake-python-styleguide", "isort"],
}

extras_require["dev"] = extras_require["test"] + extras_require["lint"]  # noqa: W504  # noqa: W504

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="fitelio-ms-client",
    author="Vyacheslav Onufrienko",
    author_email="onufrienkovi@gmail.com",
    description="Messaging service client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    url="https://gitlab.com/fitelio/messaging-service/client",
    extras_require=extras_require,
    packages=find_packages(exclude=["tests", "docs", "scripts", "example"]),
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
