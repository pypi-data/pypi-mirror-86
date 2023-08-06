# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sociallinkfinder']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'google>=3.0.0,<4.0.0',
 'rapidfuzz>=0.13.3,<0.14.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'sociallinkfinder',
    'version': '0.0.5',
    'description': "input: company's website url  , output: company's facebook, linkedin, twitter, instagram links in a dictionary",
    'long_description': "This project focuses on finding the social media links of a company by taking in as input the company's website url, using the libraries google and bs4 (beautiful soup).\n\nMost of the websites render the social media links as static HTML, but some websites render it using Javascript (dynamic websites).\n\nBeautiful Soup can only scrape static HTML code and to scrape dynamically loaded content other scraping libraries like Selenium and Scrapy+Splash will be required.\n\nTo circumvent this problem, the code also tries to find the social media links on google.\n\nSince we cannot say for sure the links returned by google may or may not belong to the company, and also when scraping a website it may return unwanted links as well, several filtering criterias are applied to return the best possible links.\n\nThe solution is not perfect and would fail to return perfect results when it is difficult to find the company's social media acoount on google and links are loaded dynamically on the official website, for example:\n\n1. The website uses a name on social media which is different than the name mentioned in the website url + links are loaded dynamically on their company's website\n2. The website doesnt have an account on a particular social media platform and someone else has an account with the name which is exactly same to the company's name",
    'author': 'Priyank Mishra',
    'author_email': 'priyank.m9320@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/priyank9320/sociallinkfinder_project',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
