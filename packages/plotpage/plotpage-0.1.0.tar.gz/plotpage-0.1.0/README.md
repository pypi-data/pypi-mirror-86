# plotpage

An alternative to Jupyter notebooks. It supports the two best things in Jupyter:
caching (achieved in Jupyter notebooks by having data loading and plotting cells)
as well as combining code, figures and output. Compared to notebooks, it's all source
code files so collaboration and reviewing is actually possible.

An HTML page is created from a Python script with stdout/stderr, figures,
and also the source code is included for effective communication.

See example.py for usage. To create the page, simply run the script with "python example.py".


## Installation with pip

Clone the repository and run `pip install -e .` from the project root.
