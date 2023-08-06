This project focuses on finding the social media links of a company by taking in as input the company's website url, using the libraries google and bs4 (beautiful soup).

Most of the websites render the social media links as static HTML, but some websites render it using Javascript (dynamic websites).

Beautiful Soup can only scrape static HTML code and to scrape dynamically loaded content other scraping libraries like Selenium and Scrapy+Splash will be required.

To circumvent this problem, the code also tries to find the social media links on google.

Since we cannot say for sure the links returned by google may or may not belong to the company, and also when scraping a website it may return unwanted links as well, several filtering criterias are applied to return the best possible links.

The solution is not perfect and would fail to return perfect results when it is difficult to find the company's social media acoount on google and links are loaded dynamically on the official website, for example:

1. The website uses a name on social media which is different than the name mentioned in the website url + links are loaded dynamically on their company's website
2. The website doesnt have an account on a particular social media platform and someone else has an account with the name which is exactly same to the company's name