import requests
from bs4 import BeautifulSoup
import urllib3
from bs4.element import Comment
from fake_useragent import UserAgent
import time
import pyfiglet
from termcolor import colored

# Font standar utk "ContentExtractor", bisa sesuaikan lebarnya jika perlu
ascii_banner = pyfiglet.figlet_format("ContentExtractor", width=100)
print(colored(ascii_banner, 'yellow'))

# Font lebih kecil utk "by Cak Mad"
ascii_banner_by = pyfiglet.figlet_format("by Cak Mad", font="digital", width=100)
print(colored(ascii_banner_by, 'yellow'))


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

url = input("Masukkan URL: ")

# Cache User-Agent utk digunakan berulang kali
ua = UserAgent()
headers = {"User-Agent": ua.random}

session = requests.Session()  # Menggunakan session requests
session.headers = headers

try:
    response = session.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.find_all(string=True)
        visible_texts = filter(tag_visible, texts)

        print("Konten Teks:")
        for text in visible_texts:
            cleaned_text = text.strip()
            if cleaned_text:
                print(cleaned_text)
                time.sleep(1)  # Delay utk setiap 10 teks

        print("Gambar:")
        for image in soup.find_all('img'):
            if 'src' in image.attrs:
                print(image['src'])
                time.sleep(1)  # Delay utk setiap 10 gambar

        print("Link:")
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                print(link['href'])
                time.sleep(1)  # Delay utk setiap 10 link
    else:
        print(f"Gagal mengakses URL dengan status: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat mengakses URL: {e}")
