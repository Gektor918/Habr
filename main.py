from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib import colors
import requests as req
from bs4 import BeautifulSoup as bes
import sqlite3 as sql
import pickle
import os

my_dict = {'\\':' ', '/':' ', ':':' ', '*':' ', '?':' ', '"':' ', '>':' ', '<':' ', '|':' '}

pdfmetrics.registerFont(TTFont('new','DejaVuSerif.ttf'))
Style=getSampleStyleSheet()

conn = sql.connect('habr.db')
cur = conn.cursor()

def main_soup(main_url):
    try:
        one_get = req.get(main_url)
        one_get.encoding='utf=8'
        soup = bes(one_get.text,'lxml')
        return soup
    except Exception as x:
        return {'error':x}

def all_snippet_link(soup,tag,**kwargs):
    m_list = ['https://habr.com'+i['href'] for i in soup.find_all(tag,**kwargs)]
    return m_list

def get_convert_binary_img(clear_img):
    all_byte_img = []
    for i in clear_img:
        r_get = req.get(i)
        img_open = open('img.jpg','wb')
        img_open.write(r_get.content)
        img_open.close()
        with open('img.jpg','rb') as new_img:
            img_byte = new_img.read()
        all_byte_img += [(img_byte)]
    return pickle.dumps(all_byte_img)

def snippet(link_snippet):
    result = []
    for link in link_snippet:
        one = main_soup(link)
        body_vers = 'article-formatted-body article-formatted-body article-formatted-body_version-1'
        try:
            one.find('div',{body_vers}).text
            print('ver-1')
        except Exception:
            body_vers = body_vers.replace('1','2')
            print('ver-2')
        date = one.find('div',{"tm-article-snippet__meta"}).find_all('span')[-1].find('time')['title'].replace(',','')
        title = one.find('title').text.rstrip()
        cont = one.find('div',{body_vers}).text
        cont_img = one.find('div',{body_vers}).find_all('img')
        clear_img = [i['src'] for i in cont_img]
        result +=[(date,title,cont,get_convert_binary_img(clear_img))]
    return result

if __name__ == '__main__':
    main_url = 'https://habr.com/ru/hub/python/'
    big_soup = main_soup(main_url)
    all_link_snippet = all_snippet_link(big_soup,'a',**{'class':'tm-article-snippet__title-link'})
result = snippet(all_link_snippet)

def update_base(result):
    new = []
    for i in result:
        cur.execute('select * from habr order by date DESC')
        if i[0] == cur.fetchall()[0][0]:
            break
        else:
            new += [(i)]
    if not new:
        return 'none'
    else:
       for i in new:    
            cur.execute("""
insert into habr (date, title, content, img) values (?,?,?,?)
""", i)
    conn.commit()
    return 'update'
update_base(result)

def my_replace(target,my_dict):
    for i,x in my_dict.items():
        target = target.replace(i,x)
    return target

def style_text():
    bt = Style['Normal']
    bt.fontName = 'new'
    bt.fontSize = 14
    bt.wordWrap = 'Normal'
    bt.firstLineIndent = 32
    bt.leading = 20
    bt.textColor = colors.black
    bt.alignment = 0
    return bt

def style_title():
    bt = Style['Normal']
    bt.fontName = 'new'
    bt.fontSize = 18
    bt.textColor = colors.chocolate
    bt.alignment = 1
    bt.spaceAfter = 5
    bt.spaceBefore = 40
    return bt

cur.execute('select * from habr order by date DESC')
all_hubs = cur.fetchall()

def create_all_pdf_and_img(all_hubs):
    num=1
    for one_hubs in all_hubs:
        one_hubs_img = pickle.loads(one_hubs[3])
        os.mkdir(my_replace(one_hubs[1],my_dict)+my_replace(one_hubs[0],my_dict))
        case = my_replace(one_hubs[1],my_dict)+my_replace(one_hubs[0],my_dict)+'//'
        for i in one_hubs_img:
            with open(case + str(num) + '.jpg','wb') as file:
                file.write(i)
                file.close()
            num += 1
        name = Paragraph(one_hubs[1],style_title())
        cont = Paragraph(one_hubs[2],style_text())
        pdf=SimpleDocTemplate(case + my_replace(one_hubs[1],my_dict)+'.pdf')
        pdf.multiBuild([name,cont])
create_all_pdf_and_img(all_hubs[:10])

