"""
Setup for qudra
"""
import os

from setuptools import setup, find_namespace_packages

REQUIREMENTS = [
    "numpy",
    "qiskit",
    "qiskit-optimization",
    "dimod",
    "matplotlib",
    "seaborn",
    "dwave-ocean-sdk",
    "dwave_networkx",
    "amazon-braket-default-simulator",
    "amazon-braket-sdk",
    "amazon-braket-ocean-plugin",
]

EXTRA_REQUIREMENTS = {
    "dev": [
        "jupyterlab>=3.1.0",
        "mypy",
        "pylint",
        "black",
        "mkdocs",
        "mkdocs-material",
        "mkdocs-gen-files",
        "mkdocs-literate-nav",
        "mkdocs-section-index",
        "mkdocstrings",
    ],
}

# Read long description from README.
README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

version_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "qudra", "VERSION.txt")
)

with open(version_path, "r") as fd:
    version_str = fd.read().rstrip()

setup(
    name="qudra",
    version=version_str,
    description="Quantum Energy Management",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Q-Energy-2022/NYUAD-2022",
    author="Asil Qraini, Fouad Afiouni, Gargi Chandrakar, Nurgazy Seidaliev, Sahar Ben Rached, Salem Al Haddad, Sarthak Prasad Malla. Mentors: Akash Kant, Shantanu Jha.",
    author_email="shantanu.rajesh.jha@gmail.com",
    license="MIT",
    packages=find_namespace_packages(exclude=["tutorials*"]),
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
    keywords="qubo energy vqe quantum computing",
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://github.com/Q-Energy-2022/NYUAD-2022",
        "Source Code": "https://github.com/Q-Energy-2022/NYUAD-2022",
        "Tutorials": "https://github.com/Q-Energy-2022/NYUAD-2022/tree/main/tutorials",
    },
    include_package_data=True,
)
