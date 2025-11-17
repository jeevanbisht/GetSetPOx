"""
Setup script for getset-pox-mcp.

This file provides backward compatibility for pip installations
that don't support pyproject.toml.
"""

from setuptools import setup, find_packages

# Read the README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="getset-pox-mcp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Model Context Protocol (MCP) server with example services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/getset-pox-mcp",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "ruff>=0.3.0",
            "mypy>=1.8.0",
        ],
        "http": [
            "uvicorn>=0.30.0",
            "starlette>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "getset-pox-mcp=getset_pox_mcp.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
