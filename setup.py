from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="hatchback",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "hatchback=hatchback.cli:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ignacio Bares",
    license="Apache-2.0",
    description="A CLI to generate a FastAPI + Alembic + SQLAlchemy boilerplate",
    keywords=[
        "fastapi-boilerplate", "fastapi-cli", "sqlalchemy-2", "production-ready-api", "pydantic-v2",
        "alembic", "docker", "clean-architecture", "rest-api", "project-generator", 
        "scaffold", "asyncio", "jwt-auth", "postgresql"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    project_urls={
        "Homepage": "https://github.com/nachovoss/hatchback",
        "Source": "https://github.com/nachovoss/hatchback",
        "Tracker": "https://github.com/nachovoss/hatchback/issues",
    },
)
