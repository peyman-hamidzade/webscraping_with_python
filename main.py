import requests
from bs4 import BeautifulSoup
import re



def check_url(url):
    '''check the url is correct or not'''
    pattern = r'^(http|https):\/\/[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None



def scrape_data(url):
    ''' send a request to url and return the data'''
    data = []

    if check_url(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        product_list = soup.find_all("div", class_="kt-post-card__info")

        for product in product_list:
            description_elements = product.find_all("div", class_="kt-post-card__description")
            karkard = description_elements[0].text
            price = description_elements[1].text.strip()
            name = product.find("h2", class_="kt-post-card__title").text

            data.append({'نام': name, 'قیمت': price, 'کارکرد':karkard})
    else:
        print("invalid url")

    return data



def save_as_html(data):
    '''make a file from data and seve it on product_data.html'''
    with open('product_data.html', mode='w', encoding='utf-8') as file:
        file.write('<html dir="rtl">\n<body>\n')
        for product_entry in data:
            file.write(f"<p>{' | '.join(f'{key}: {value}' for key, value in product_entry.items())}</p><br>")

    print("Data saved successfully.")


if __name__ == "__main__":
    url = None
    while not url:
        url = input("Please enter a URL: ")
        if not check_url(url):
            print("Invalid URL. Please try again.")
            url = None
    
    scraped_data = scrape_data(url)
    
    if scraped_data:
        save_as_html(scraped_data)