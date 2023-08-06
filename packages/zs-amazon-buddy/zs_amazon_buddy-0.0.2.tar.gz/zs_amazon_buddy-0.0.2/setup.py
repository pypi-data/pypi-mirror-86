import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'amazon_buddy'

setuptools.setup(
    name="zs_amazon_buddy",
    version="0.0.2",
    author="Kristof & Zselter",
    description="python wrapper for the amazon_buddy npm package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/py_amazon_buddy",
    packages=setuptools.find_packages(),
    install_requires=["randomua", "kcu", "Unidecode", "requests", "jsoncodable", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)