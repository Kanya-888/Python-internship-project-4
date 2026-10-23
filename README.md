# Python-internship-project-4

# Project 04: Web Scraper for Quotes

## About
A Python web scraper that collects quotes, authors, and tags from
the practice website quotes.toscrape.com.

## Features
- Sends HTTP requests using requests
- Parses HTML using BeautifulSoup
- Extracts quote text, author, and tags
- Follows pagination to collect multiple pages
- Handles HTTP errors, timeouts, and network failures
- Saves the results to JSON and readable text files
- Reports the total quotes, most quoted author, and most common tag

## Requirements
Python 3.10 or newer.

Install dependencies:

python -m pip install requests beautifulsoup4

## How to Run
Run this command in the project folder:

python project4.py

## Output Files
- quotes.json: structured quote records
- quotes.txt: readable quote records

## Data Source
https://quotes.toscrape.com/

This practice website is designed for learning web scraping.

## Politeness and Responsible Scraping
- Uses a descriptive User-Agent header
- Sets a request timeout
- Waits one second between page requests
- Limits the run to 20 pages
- Does not access login-protected pages or collect personal data
