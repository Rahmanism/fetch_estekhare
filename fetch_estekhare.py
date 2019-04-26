import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


def parse_estekhare_data(soup, container_box):
    """
    Parses the html from estekhare.net
    """
    container = soup.find('div', {'id': container_box})
    result = container.find('h1').text
    address = container.find('h6').text.split()
    if str.endswith(container_box, '1'):
        # finglish
        sure_no = int(address[0][6:-1])
        aye_no = int(address[1][6:-1])
    elif str.endswith(container_box, '2'):
        # farsi
        sure_no = int(address[0][6:-1])
        aye_no = int(address[1][5:-1])
    else:
        # english
        sure_no = int(address[0][7:-1])
        aye_no = int(address[1][6:-1])
    h2s = container.find_all('h2')
    comment = h2s[0].text
    sure = h2s[1].contents[0].split()
    sure = ' '.join(sure[1:])
    aye = h2s[1].contents[2]
    return {
        'result': result,
        'comment': comment,
        'sure': sure,
        'aye': aye,
        'sure_no': sure_no,
        'aye_no': aye_no
    }


def get_estekhare_data():
    url = 'http://estekhare.net/index2.php'
    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')

    finglish_box = 'newboxes1'
    farsi_box = 'newboxes2'
    english_box = 'newboxes3'

    finglish = parse_estekhare_data(soup, finglish_box)
    farsi = parse_estekhare_data(soup, farsi_box)
    english = parse_estekhare_data(soup, english_box)

    return {
        'finglish': finglish,
        'farsi': farsi,
        'english': english
    }
