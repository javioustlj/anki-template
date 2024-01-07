import json
import urllib.request
from bs4 import BeautifulSoup

def get_vocabulary_definition(note):
    expression = note['expression']
    url = 'https://www.vocabulary.com/dictionary/{0}'.format(expression)
    print(url)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode(), 'lxml')
    note['short'] = u''
    note['long'] = u''
    element = soup.find('p', class_='short')
    if element:
        note['short'] = u''.join(str(element.get_text()))
    element = soup.find('p', class_='long')
    if element:
        note['long'] = u''.join(str(e) for e in element.get_text())

def get_definitions(notes):
    for note in notes:
        if (' ' not in note['expression']):
            get_vocabulary_definition(note)
        print(note)

def main():
    with open('test.json', 'r') as f:
        notes = json.loads(f.read())
    get_definitions(notes)

if __name__ == '__main__':
    main()