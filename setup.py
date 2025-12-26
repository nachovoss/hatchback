from setuptools import setup, find_packages

setup(
    name="fast-boilerplate",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # No runtime dependencies for the CLI itself
    ],
    entry_points={
        "console_scripts": [
            "fast-boilerplate=fast_boilerplate.cli:init_project",
        ],
    },
    author="Ignacio Bares",
    description="A CLI to generate a FastAPI + Alembic + SQLAlchemy boilerplate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
