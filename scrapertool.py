import requests
from bs4 import BeautifulSoup

def scrape(site):
    try:
        print(f"Mulai melakukan scraping pada situs: {site}")
        page = requests.get(site)
        page.raise_for_status()  # Menyebabkan error jika permintaan gagal
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            result_text = f"Alamat Link: {link_address}, Teks Link: {link_text}"
            print(result_text)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong", err)

def main():
    site = input("Masukkan alamat URL yang ingin discrape: ")
    scrape(site)
    print("=========================")
    print("Created by Ariful")

if __name__ == "__main__":
    main()
