#! python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, string, unicodedata

CITATION_REGEX = re.compile('\[[0-9]*\]')
PARENS_REGEX = re.compile('\([a-z A-Z \+\.,\-]{0,100}\)')
DESCRIPTION_REGEX = re.compile('\n[a-z A-Z]*:')

puncts = [re.escape(c) for c in string.punctuation]
PUNCTUATION_REGEX = re.compile('|'.join(puncts))
#PUNCTUATION_REGEX = re.compile('[' + re.escape(''.join(puncts)) + ']')

url = 'http://en.wikipedia.org/wiki/Python_(programming_language)'
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')

content = bs.find('div', {'id':'mw-content-text'}).find_all('p')
content = [p.get_text() for p in content]
content = ''.join(content)

def replace_newlines(text):
    return text.replace('\n',' ')
    #pass

def make_lowercase(text):
    return [t.lower() for t in text]
    #pass

def split_sentences(text):
    return [s.strip() for s in text.split('. ')]
    #pass

def strip_citations(text):
    return re.sub(CITATION_REGEX, '', text)
    #pass

def remove_parentheses(text):
    return re.sub(PARENS_REGEX, '', text)
    #return re.sub('\([a-z A-Z \+\.,\-]{0,100}\)', '', text)
    #pass

def remove_descriptions(text):
    return re.sub(DESCRIPTION_REGEX, '', text)
    #pass

def remove_punctuation(text):
    return re.sub(PUNCTUATION_REGEX, '', text)
    #pass

def normalize(text):
    return unicodedata.normalize('NFKD', text)
    #pass

text_operations = [
    strip_citations, 
    remove_parentheses, 
    remove_descriptions, 
    replace_newlines, 
    split_sentences, 
    make_lowercase, 
    remove_punctuation, 
    normalize
]

cleaned = content
for op in text_operations:
    print(type(cleaned))
    if type(cleaned) == list:
        cleaned = [op(c) for c in cleaned]
    else:
        cleaned = op(cleaned)
    print(cleaned)
        
print(cleaned)