import os
import re
from setuptools import setup, find_packages

def get_version(package):
    path = os.path.join(package, "__init__.py")
    with open(path, "r", encoding="utf8") as f:
        init_py = f.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

setup(
    name="aicommit",
    version=get_version("aicommit/src"),  # <-- updated path
    description="An AI-powered git commit message generator!",
    long_description="AI-powered git commit message generator.",
    long_description_content_type="text/markdown",
    packages=find_packages(where="aicommit"),  # <-- look inside aicommit/
    package_dir={"": "aicommit"},              # <-- base package dir
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "inquirer>=3.1.2",
        "openai>=1.1.0",
        "python-dotenv>=0.21.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "aicommit=src.aicommit:main",
        ],
    },
)
