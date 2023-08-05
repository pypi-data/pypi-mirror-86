import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FilterReportIPsByCount", 
    version="1.0.1",
    author="Divyaa Kamalanathan",
    author_email="divyaa.kamalanathan@intrinium.com",
    description="Script to read through a report, grab IPs and check if malicious, output-ing malicious IP information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divyaaveerama/FilterReportIPsByCount",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
