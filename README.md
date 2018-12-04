# Ultimate Guitar Web Scraper

This is a scraper implemented in python to scrape chord progressions from the website ultimate-guitar.com. The scraper works
as a web crawler, where a seed page is given and the data is then scraped systematically by traversing all the links on the 
page. Once a page with chord progressions is found, the data is scraped and then saved to a json file.

The ultimate goal of this project was to scrape enough songs to seed a markov chain based on chord progressions.
