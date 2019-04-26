import requests
from bs4 import BeautifulSoup


def get_estekhare_data(soup, container_box):
    container = soup.find('div', {'id': container_box})
    result = container.find('h1').text
    address = container.find('h6').text.split()
    print(address)
    if str.startswith(container_box, 'fi'):
        sure_no = int(address[0][7:-1])
        aye_no = int(address[1][6:-1])
    elif str.startswith(container_box, 'fa'):
        sure_no = int(address[0][6:-1])
        aye_no = int(address[1][5:-1])
    else: # en
        sure_no = int(address[0][7:-1])
        aye_no = int(address[1][6:-1])
    h2s = container.find_all('h2')
    comment = h2s[0].text
    sure = h2s[1].contents[0]
    aye = h2s[1].contents[2]
    return {
        'result': result,
        'comment': comment,
        'sure': sure,
        'aye': aye,
        'sure_no': sure_no,
        'aye_no': aye_no
    }


url = 'http://estekhare.net/index2.php'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

finglish_box = 'newboxes1'
farsi_box = 'newboxes2'
english_box = 'newboxes3'

finglish = get_estekhare_data(soup, finglish_box)
farsi = get_estekhare_data(soup, farsi_box)
english = get_estekhare_data(soup, english_box)

print(finglish)
print(farsi)
print(english)
