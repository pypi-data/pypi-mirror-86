import os
import setuptools
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

about = {}
print(os.path.join(here, "paddock", "__version__.py"))
with open(os.path.join(here, 'paddock', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about.get("__version__", "0.0.0.dev0"),
    description=about["__description__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    packages=setuptools.find_packages(
        exclude=[
            "tests", "*.tests", "*.tests.*",
            "integration_tests", "*.integration_tests",
            "*.integration_tests.*",
        ]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "decorator>=4.4.2,<5",
        "requests>=2.24,<3",
        "marshmallow-dataclass>=7.2,<8",
        "marshmallow-enum>=1.5,<2",
        "marshmallow-oneofschema>=2.0,<3",
        "marshmallow>=3.3,<4",
    ],
)
