from setuptools import find_packages, setup

setup(
    name="plotpage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["jinja2", "mypy", "matplotlib", "markdown2"],
    include_package_data=True,
    package_data={'': ['highlight-github.css', 'highlight.pack.js']}
)
