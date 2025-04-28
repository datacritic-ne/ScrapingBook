#! python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import random, datetime, re
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='j@Gr71JV1L3',
    db='mysql',
    charset='utf8'
)
cur = conn.cursor()
cur.execute('USE scraping')
#cur.execute('SELECT * FROM pages WHERE id=1')
#print(cur.fetchone())
#cur.close()
#conn.close()

currentTime = datetime.datetime.now()
random.seed(int(currentTime.timestamp()))

def store(title, content):
    cur.execute('INSERT INTO pages (title, content) VALUES ' '("%s", "%s")', (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org'+articleUrl)
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.find('h1').get_text()
    content = bs.find('div', {'id':'mw-content-text'}). find('p').get_text()
    store(title, content)
    return bs.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/Kevin_Bacon')
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()