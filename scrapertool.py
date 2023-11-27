import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import pyfiglet
from termcolor import colored

# Buat ASCII art utk teks "SCRAPER"
ascii_banner = pyfiglet.figlet_format("SCRAPER")
print(colored(ascii_banner, 'yellow'))  # Mencetak "SCRAPER" dalam huruf kapital berukuran besar dan berwarna kuning
print(colored("Created by Cak Mad", 'green'))  # Mencetak "Created by Cak Mad" berwarna hijau terang


def clean_url(url):
    # Membersihkan URL dari query string untuk menghindari duplikasi karena parameter yang berubah
    parsed_url = urlparse(url)
    cleaned_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return cleaned_url

def scrape(site, depth=2, output_file="output.txt"):
    visited = set()
    queue = deque([(site, 0)])

    with open(output_file, "w") as file:
        while queue:
            current_url, current_depth = queue.popleft()
            if current_depth > depth:
                break

            try:
                page = requests.get(current_url)
                page.raise_for_status()
                soup = BeautifulSoup(page.text, 'html.parser')

                cleaned_current_url = clean_url(current_url)
                if cleaned_current_url in visited:
                    continue

                visited.add(cleaned_current_url)
                file.write(cleaned_current_url + "\n")
                print(f"Level: {current_depth}, URL: {cleaned_current_url}")

                for link in soup.find_all('a'):
                    link_address = link.get('href')
                    if link_address and not link_address.startswith('#'):
                        full_link = urljoin(current_url, link_address)
                        cleaned_full_link = clean_url(full_link)
                        if cleaned_full_link not in visited:
                            queue.append((cleaned_full_link, current_depth + 1))

            except requests.RequestException as e:
                print(f"Error pada {current_url}: {e}")

def main():
    site = input("Masukkan alamat URL yang ingin discrape: ")
    scrape(site)
    print("=========================")
    print(colored("Thanks for support, Cak Mad", 'red'))

if __name__ == "__main__":
    main()
