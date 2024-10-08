import os
import requests
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style, init


#Inicializamos colorama
init(autoreset=True)

class Username:
    def user(self):
        self.name = input(Fore.YELLOW + 'Escribe el nombre: ')
        return self.name

class Url:
    def __init__(self, username):
        self.username = username

    def url_form(self):
        base_url = 'https://www.google.com/search?tbm=isch'
        encoded_query = quote(self.username)
        self.url = f'{base_url}&q={encoded_query}'
        print(Fore.GREEN + f"Searching.... {self.url}")
        return self.url

class Get_image:
    def extract_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(src=True)
            base_url = url
            srcs = [urljoin(base_url, element['src']) for element in elements]
            if srcs:
                srcs.pop(0) #Elimina la primera entrada src
            return srcs
        except requests.RequestException as e:
            print(Fore.RED + f'Error en la solicitud: {e}')
            return []

    def download_images(self, srcs, output_dir='imagenes'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i, src in enumerate(srcs):
            file_name = os.path.join(output_dir, f'imagen_{i + 1:02}.jpg')
            self.download_image(src, file_name)
    
    def download_image(self, url, file_name):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f'Downloading... {file_name}')
        except requests.RequestException as e:
            print(Fore.RED + f'Error al descargar la imagen: {e}')

def main():
    print("Starting....")
    u = Username()
    name = u.user()
    u2 = Url(name)
    url = u2.url_form()
    img = Get_image()
    srcs = img.extract_url(url)
    if srcs:
        print("Downloading images....")
        img.download_images(srcs)

if __name__ == "__main__":
    main()

