import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sitemap-range-fetch",
    version="0.9.5",
    author="Stefan Corneliu Petrea",
    author_email="stefan@garage-coding.com",
    description="Sitemap scraper for news article selection within a certain time range",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.garage-coding.com/",
    packages=setuptools.find_packages(),
    scripts=["sitemap_fetch.py"],
    install_requires=[
          'lxml>=4.3.2',
          'requests>=2.21.0',
          'beautifulsoup4>=4.9.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
