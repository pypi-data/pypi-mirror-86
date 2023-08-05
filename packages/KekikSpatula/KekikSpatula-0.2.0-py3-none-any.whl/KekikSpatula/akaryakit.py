# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import requests
from bs4 import BeautifulSoup

from KekikSpatula.Statik import Statik

class Akaryakit(Statik):
    """
    Akaryakit : finans.haberler.com adresinden akaryakıt verilerini hazır formatlarda elinize verir.

    Methodlar
    ----------
        .veri()         -> dict:
            json verisi döndürür.

        .gorsel()       -> str:
            oluşan json verisini insanın okuyabileceği formatta döndürür.

        .tablo()        -> str:
            tabulate verisi döndürür.

        .anahtarlar()   -> list:
            kullanılan anahtar listesini döndürür.
    """
    def __init__(self):
        "akaryakıt verilerini finans.haberler.com'dan alarak bs4'ile ayrıştırır."

        kaynak  = "finans.haberler.com"
        url     = "https://finans.haberler.com/akaryakit/"
        kimlik  = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        istek   = requests.get(url, headers=kimlik)

        corba   = BeautifulSoup(istek.content, "lxml")

        son_guncellenme = corba.select('body > div > div.hbMain.stickyNo > div:nth-child(3) > div > div.col696 > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text
        cerceve         = corba.find('div', class_='hbTableContent piyasa')

        kekik_json = {"kaynak": kaynak, 'son_guncellenme': son_guncellenme, 'veri' : []}

        for tablo in cerceve.findAll('tr')[1:]:
            cinsi  = tablo.find('td', {'width' : '50%'}).text.replace(' TL',' -- ₺')
            fiyati = tablo.find('td', {'width' : '16%'}).text

            kekik_json['veri'].append({
                'cinsi'     : cinsi,
                'fiyati'    : fiyati
            })

        self.kekik_json  = kekik_json if kekik_json['veri'] != [] else None