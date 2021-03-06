import requests
from bs4 import BeautifulSoup as bs
import csv

def get_book_page(book_url):
    # Connexion au serveur de façon générique
    url = book_url
    response = requests.get(url)

    # On parse le contenu HTML obtenu
    soup = bs(response.content, 'html.parser')
    # Extraction des éléments de la table contenant les headers

    table = soup.find('table', class_='table table-striped')
    # print(table)
    upc = table.find('tr').td.text.strip('\n')
    product_type = table.find('tr').find_next_siblings()[0].get_text().strip('\n')
    price_excluding_tax = table.find('tr').find_next_siblings()[2].td.text
    price_including_tax = table.find('tr').find_next_siblings()[3].td.text
    number_available = table.find('tr').find_next_siblings()[4].td.text
    review_rating = table.find('tr').find_next_siblings()[5].td.text
    category = soup.find('ul', class_='breadcrumb').li.find_next_siblings()[1].text
    # print(category)
    # Ajout de la colonne description
    product_description = soup.find('div', class_='sub-header').find_next_siblings()[0].text.strip('\n')

    # Ajout de la colonne title
    title = soup.find('div', class_='col-sm-6 product_main').h1.text.strip('\n')

    # Ajout de la colonne image_url
    image = soup.find('div', class_='item active')
    for image in image.find_all('img'):
        image_url = image['src']

    # Récupération de l'URL de la page produit
    product_page_url = soup.find('ul', class_='breadcrumb').find_all('a')[2]['href']

    data = {
        'product_page_url': product_page_url,
        'upc': upc,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'product_type': product_type,
        'review_rating': review_rating,
        'image_url': image_url,
        'category': category
    }
    return data