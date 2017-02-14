import orodja
import re

parametri = ['226.Favorite_books_from_my_childhood', '651.What_Book_Got_You_Hooked_', '86.Best_Children_s_Books']


for i in range(len(parametri)):
        osnovni_naslov = 'http://www.goodreads.com/list/show/' + parametri[i]
        for stran in range(1, 13):
            naslov = '{}?&page={}'.format(osnovni_naslov, stran)
            ime_datoteke = 'lista' + str(i+1) + '/{:02}.html'.format(stran)
            orodja.shrani(naslov, ime_datoteke)


def pocisti_podatke(knjiga):
    podatki = knjiga.groupdict()
    podatki['id_nasl'] = int(podatki['id_nasl'])
    podatki['mesto'] = int(podatki['mesto'])
    podatki['id_avt'] = int(podatki['id_avt'])
    podatki['ocena'] = float(podatki['ocena'])
    podatki['st_glasov'] = int(podatki['st_glasov'].replace(',', ''))
    podatki['ocena_skupaj'] = int(podatki['ocena_skupaj'].replace(',', ''))
    return podatki

def pocisti_podatke1(naslov):
    podatki = naslov.groupdict()
    podatki['id_nasl'] = int(podatki['id_nasl'])
    return podatki

def pocisti_podatke2(avtor):
    podatki = avtor.groupdict()
    podatki['id_avt'] = int(podatki['id_avt'])
    return podatki

def cisti(tabela):
   seen = set()
   new_l = []
   for d in tabela:
      t = tuple(d.items())
      if t not in seen:
        seen.add(t)
        new_l.append(d)
   return new_l


regex_knjige = re.compile(
        r'<td valign="top" class="number">(?P<mesto>\d+)</td>.*?'
        r'<a class="bookTitle".*?book/show/(?P<id_nasl>\d+).*?>.*?'
        r'<a class="authorName".*?author/show/(?P<id_avt>\d+).*?>.*?'
        r'</span></span> (?P<ocena>\d+\.?\d*) avg rating.*?(?P<st_glasov>\d+,?\d*,?\d*) ratings</span>.*?'
        r'score: (?P<ocena_skupaj>\d+,?\d*)</a>',
        flags=re.DOTALL
    )

regex_naslov = re.compile(
        r'<a class="bookTitle".*?book/show/(?P<id_nasl>\d+).*?<span itemprop.*?>(?P<naslov>.*?)</span>',
        flags=re.DOTALL
    )

regex_avtor = re.compile(
        r'<a class="authorName".*?author/show/(?P<id_avt>\d+).*?><span itemprop.*?>(?P<avtor>.*?)</span>',
        flags=re.DOTALL
    )



naslovi = []
avtorji = []
for i in range(3):
        knjige = []
        for html_datoteka in orodja.datoteke( 'lista' + str(i + 1) + '/'):
            for knjiga in re.finditer(regex_knjige, orodja.vsebina_datoteke(html_datoteka)):
                knjige.append(pocisti_podatke(knjiga))
            for naslov in re.finditer(regex_naslov, orodja.vsebina_datoteke(html_datoteka)):
              naslovi.append(pocisti_podatke1(naslov))
            for avtor in re.finditer(regex_avtor, orodja.vsebina_datoteke(html_datoteka)):
              avtorji.append(pocisti_podatke2(avtor))


        orodja.zapisi_tabelo(knjige, ['mesto','id_nasl', 'id_avt', 'ocena', 'st_glasov', 'ocena_skupaj'], 'tabela' + str(i + 1) + '.csv')



tabela_naslovi = cisti(naslovi)
tabela_avtorji = cisti(avtorji)
orodja.zapisi_tabelo(tabela_naslovi, ['id_nasl', 'naslov'], 'naslov.csv')
orodja.zapisi_tabelo(tabela_avtorji, ['id_avt','avtor'], 'avtor.csv')

