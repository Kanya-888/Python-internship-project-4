
import json
import time
from collections import Counter
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "InternCircleLearningProject/1.0 (educational scraper)"
}
REQUEST_DELAY = 1
MAX_PAGES = 20


def scrape_quotes():
    """Fetch quotes from the practice website, one page at a time."""
    url = BASE_URL
    quotes = []
    visited_urls = set()

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for page_number in range(1, MAX_PAGES + 1):
            if not url or url in visited_urls:
                break

            visited_urls.add(url)
            print(f"Fetching page {page_number}: {url}")

            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()

            except requests.exceptions.Timeout:
                print("Request timed out. Stopping the scraper.")
                break

            except requests.exceptions.HTTPError as error:
                print(f"HTTP error: {error}")
                break

            except requests.exceptions.RequestException as error:
                print(f"Network error: {error}")
                break

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract each quote, author, and tag
            for quote_box in soup.select("div.quote"):
                text_element = quote_box.select_one("span.text")
                author_element = quote_box.select_one("small.author")

                # Avoid crashing if the website structure changes
                if text_element is None or author_element is None:
                    continue

                quote_data = {
                    "text": text_element.get_text(strip=True),
                    "author": author_element.get_text(strip=True),
                    "tags": [
                        tag.get_text(strip=True)
                        for tag in quote_box.select("a.tag")
                    ]
                }

                quotes.append(quote_data)

            # Find the Next page link
            next_link = soup.select_one("li.next a")

            if next_link is None:
                print("No more pages.")
                break

            url = urljoin(url, next_link.get("href", ""))

            # Be polite: wait before requesting another page
            if page_number < MAX_PAGES:
                time.sleep(REQUEST_DELAY)

    return quotes


def save_json(quotes, filename="quotes.json"):
    """Save extracted quotes as formatted JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)


def save_text(quotes, filename="quotes.txt"):
    """Save quotes in a readable text format."""
    with open(filename, "w", encoding="utf-8") as file:
        for number, quote in enumerate(quotes, start=1):
            file.write(f"Quote {number}\n")
            file.write(f"Text: {quote['text']}\n")
            file.write(f"Author: {quote['author']}\n")
            file.write(f"Tags: {', '.join(quote['tags']) or 'None'}\n")
            file.write("-" * 60 + "\n")


def print_summary(quotes):
    """Print total quotes, most quoted author, and common tag."""
    print("\n" + "=" * 50)
    print("SCRAPING SUMMARY")
    print("=" * 50)
    print(f"Total quotes collected: {len(quotes)}")

    if not quotes:
        print("No quotes were collected. Check your internet connection.")
        return

    author_counts = Counter(
        quote["author"] for quote in quotes if quote["author"]
    )

    tag_counts = Counter(
        tag for quote in quotes for tag in quote["tags"]
    )

    if author_counts:
        author, count = author_counts.most_common(1)[0]
        print(f"Most quoted author: {author} ({count} quotes)")

    if tag_counts:
        tag, count = tag_counts.most_common(1)[0]
        print(f"Most common tag: {tag} ({count} occurrences)")
    else:
        print("No tags were found.")

    print("=" * 50)


def main():
    print("WEB SCRAPER FOR QUOTES")
    print("Source:", BASE_URL)

    try:
        quotes = scrape_quotes()

        save_json(quotes)
        save_text(quotes)

        print(f"\nSaved {len(quotes)} quotes to quotes.json")
        print(f"Saved {len(quotes)} quotes to quotes.txt")

        print_summary(quotes)

    except OSError as error:
        print(f"Could not save output files: {error}")


if __name__ == "__main__":
    main()
