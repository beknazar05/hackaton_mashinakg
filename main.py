import csv 
import requests
import lxml
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html:str) -> None:
    soup = BeautifulSoup(html,'lxml')
    catalog = soup.find('div',class_='search-results-table')
    cars = catalog.find_all('div',class_='list-item')
    for car in cars:
        try:
            name = car.find('h2', class_='name').text.strip()
        except:
            name = 'No Name'
        try:
            price = car.find('div',class_='block price').find('strong').text.strip()
        except:
            price = 'No price'
        try:
            info = car.find('div',class_='block info-wrapper item-info-wrapper')
            year = info.find('p',class_='year-miles').text.strip()
            type_car = info.find('p',class_='body-type').text.strip()
            volume = info.find('p',class_='volume').text.strip()
            res = f'{year},{type_car},{volume}'
        except:
            res = 'No info'
        try:
            image = car.find('a').find('img').get('data-src')
            # img_link = car.find('div',class_='tmb-wrap')
        except:
            image = 'No photo'
        data = {
            'name': name,
            'price': price,
            'res': res,
            'photo': image
        }
        write_to_csv(data)


def write_to_csv(data:dict) -> None:
    import csv
    with open('cars.csv','a') as file:
        fieldnames = ['Title','Price','Info','Photo']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writerow({
            'Title': data.get('name'),
            'Price' : data.get('price'),
            'Info': data.get('res'),
            'Photo':data.get('photo')
        })



def main():
    i = 1
    while True:
        print(f'Выполнено страниц{i}')
        url = f'https://www.mashina.kg/search/all/all/?currency=2&sort_by=upped_at+desc&time_created=all&page={i}'
        html = get_html(url)
        get_data(html)
        catalog = BeautifulSoup(html,'lxml').find('div',class_='search-results-table')
        if not catalog:
            break
        get_data(html)
        i += 1 
main()