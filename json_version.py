import requests
from bs4 import BeautifulSoup as bs
import json


base_url = 'http://continewsnv5otx5kaoje7krkto2qbu3gtqef22mnr7eaxw3y6ncz3ad.onion'

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

urls = []
full_data = []


def get_html(url):
    r = requests.get(url, proxies=proxies)
    if r.ok:
        return r.text
    print(r.status_code)


def get_json(url):
    r = requests.get(url, proxies=proxies)
    if r.ok:
        return r.json()
    print(r.status_code)


def get_url(html):
    soup = bs(html, 'lxml')
    head = soup.find_all('div', class_='card')

    for h in head:
        try:
            url = h.find('div', class_='footer').find('a').get('href').strip('/').split('_')[0]
        except AttributeError:
            url = None

        urls.append(url)


def get_file(data):
    return [base_url + f"/files/{data['code']}/{j[0]}" for j in data['files']]


def get_file_data():
    pattern = 'http://continewsnv5otx5kaoje7krkto2qbu3gtqef22mnr7eaxw3y6ncz3ad.onion/?get={}'
    for i in urls:
        url = pattern.format(i)
        data = get_json(url)
        d = {
            'url': base_url + data['url'],
            'name': data['title'],
            'date': data['date'],
            'url_company': data['link'],
            'description': data['text'],
            'file': get_file(data),
        }

        full_data.append(d)


def main():
    pattern = 'http://continewsnv5otx5kaoje7krkto2qbu3gtqef22mnr7eaxw3y6ncz3ad.onion/page/{}'

    for i in range(1, 2):
        url = pattern.format(str(i))
        get_url(get_html(base_url))
        get_file_data()
    with open('file.json', 'w') as f:
        json.dump(c, f, indent=2)


if __name__ == '__main__':
    main()
