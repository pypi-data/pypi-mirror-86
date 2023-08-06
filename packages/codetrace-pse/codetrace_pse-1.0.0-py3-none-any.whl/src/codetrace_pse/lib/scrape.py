import requests
from bs4 import BeautifulSoup as bs

URL = "https://www.pesobility.com/stock/{sym}"


def parse_table(table_data):
    """Method that parses the main table that contains the
    required information.
    :param table_data: soup html object to parse
    :return: tuple; parsed data
    """
    # 1st row
    row_1 = table_data[1].find_all('div')
    curr_price = row_1[1].find('span').text.strip()
    prev_close = row_1[3].find('span').text.strip()
    # 3rd row
    row_3 = table_data[3].find_all('div')
    open_ = row_3[1].text.strip()
    # 4th row
    row_4 = table_data[4].find_all('div')
    volume = row_4[1].text.strip()
    # 6th row
    row_6 = table_data[6].find_all('div')
    high_52_week = row_6[1].text.strip()
    low_52_week = row_6[3].text.strip()
    # 7th row
    row_7 = table_data[7].find_all('div')
    shares = row_7[1].text.strip()

    return curr_price, prev_close,\
        open_, volume, high_52_week,\
        low_52_week, shares


def get_info(symbol: str):
    """Method that gets stock exchange data from the 'URL' by
    parsing the HTML content of the page.
    :param symbol: string; stock symbol
    :return: dict; parsed data
    """
    try:
        url = URL.replace('{sym}', symbol.upper())
        content = requests.get(url)
        if content.status_code == 200:
            soup = bs(content.text, 'html.parser')
            body = soup.find('div', class_='gray-bg main-body')
            name = body.find('h2', class_='subheader').text.strip()
            table_data = body.find_all('div', class_='row')
            p = parse_table(table_data)
            return {
                'status': 'OK', 'name': name, 'source_url': url,
                'curr_price': p[0], 'prev_price': p[1],
                'open': p[2], 'volume': p[3],
                'high_52_week': p[4], 'low_52_week': p[5],
                'shares': p[6], 'sym': f"{symbol}",
            }
        elif content.status_code == 404:
            return {'status': f"Unable to find stock details: "
                              f"'{symbol}'"}
        else:
            return {'status': f'Unexpected error encountered: '
                              f'{content.status_code}'}
    except Exception as ex:
        return {'status': f'Exception encountered: {ex}'}
