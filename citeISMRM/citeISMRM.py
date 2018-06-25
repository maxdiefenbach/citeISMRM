#!/usr/bin/env python

import argparse
import urllib.request
from bs4 import BeautifulSoup
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import webbrowser


def main():
    """
    commandline tool to extract bibtex entries
    for ISMRM abstracts from
    https://archive.ismrm.org

    example usage:
    $ python main.py -y 2017 -n 850 # prints bibtex entry
                                         # from 2017 abstract #0850 to stdout

    $ python main.py -y 2017 -n 850 -w abstract.bib
    # writes bibtex entry to file abstract.bib

    $ python main.py -y 2017 -n 850 -a bibliography.bib
    # appends bibtex entry to file bibliography.bib

    see $ python main.py --help for more
    """
    parser = argparse.ArgumentParser(
        description='Create bibtex for ISMRM abstract.')
    parser.add_argument('-y', '--year', type=int, help='year')
    parser.add_argument('-n', '--number', type=int,
                        help='number (in the proceedings)')
    parser.add_argument('-l', '--link', help='abstract link')
    parser.add_argument('-w', '--write', help='write to file')
    parser.add_argument('-wd', '--write-default', action='store_true')
    parser.add_argument('-a', '--append', help='append to file')
    args = parser.parse_args()

    if args.link is None and \
       (args.year is None and args.number is None):
        parser.print_help()
        return

    if args.link:
        link = args.link
    else:
        link = getAbstractUrl(args.year, args.number)

    print(link)
    abstractDict = getAbstractDictFromUrl(link)
    bibtex_str = getBibtexStrFromAbstractDict(abstractDict)

    if args.write:
        filename = args.write
        filemode = 'w'
    elif args.append:
        filename = args.append
        filemode = 'a'
    elif args.write_default:
        filename = abstractDict['ID'] + '.bib'
        filemode = 'w'
    else:
        filename = None
        filemode = None

    if filemode and filename:
        with open(filename, filemode) as f:
            f.write(bibtex_str)
        print('Wrote bibtex to file {}.'.format(filename), end='')
    else:
        print(bibtex_str, end='')

    return 0


def getAbstractDictFromUrl(url):
    if type(url) is list:
        dictList = []
        for u in url:
            dictList.append(getAbstractDictFromUrl(u))
        return dictList
    else:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
        year = url.split('/')[-2]
        pages = url.split('/')[-1][:-5]
        journal = 'Annual Meeting International Society ' \
                  'for Magnetic Resonance in Medicine'
        if year == '2011':
            title = soup.find('h1').string.replace('\n ', '')
            author = soup.find('p', {'class': 'ISMRMAuthors'}).get_text()
            volume = 19
            address = "Montreal, Canada"
        elif year == '2012':
            title = soup.find('h1').string.replace('\n ', '')
            author = soup.find('p', {'class': 'ISMRMAuthors'}).get_text()
            volume = 20
            address = "Melbourne, Australia"
        elif year == '2013':
            webbrowser.open(url)
            raise NameError('not yet determined? year {}'.format(year))
        elif year == '2014':
            title = soup.find('h1').string.replace('\n ', '')
            author = soup.body.h1.findNext('div').\
                get_text().replace('  ', '').replace('\t', '')
            volume = 22
            address = "Milan, Italy"
        elif year == '2015':
            title = soup.find('h1').string.replace('\n ', '')
            author = soup.body.h1.findNext('div').\
                get_text().replace('  ', '').replace('\t', '')
            volume = 23
            address = "Toronta, Canada"
        elif year == '2016':
            title = soup.find('h1').string
            author = soup.find(id='affAuthers').get_text()
            volume = 24
            address = "Singapore"
        elif year == '2017':
            title = soup.find('h1').string
            author = soup.find(id='affAuthers').get_text()
            volume = 25
            address = "Honolulu, Hawaii"
        elif year == '2018':
            title = soup.find('h1').string
            author = soup.find(id='affAuthers').get_text()
            volume = 26
            address = "Paris, France"
        else:
            webbrowser.open(url)
            raise NameError('not yet determined? year {}'.format(year))
        if title is None:
            raise NameError('abstract {} {} not found.'.format(year, pages))
        abstractDict = {'title': title,
                        'author': ''.join(c for c in author
                                           if not c.isdigit()),
                        'year': year,
                        'volume': str(volume),
                        'journal': journal,
                        'address': address,
                        'pages': pages,
                        'url': url}
        abstractDict['ENTRYTYPE'] = 'inproceedings'
        abstractDict['ID'] = abstractDict['author'].\
            split(',')[0].split(' ')[-1] + \
            '_ISMRM' + abstractDict['year'] + '_' + \
            abstractDict['pages']
        abstractDict['title'] = '{' + abstractDict['title'] + '}'
        abstractDict['author'] = abstractDict['author'].\
                                 replace(',', ' and').\
                                 replace('and and', 'and').\
                                 replace('  and', ' and')
        abstractDict['booktitle'] = 'Proceedings ' + abstractDict['volume'] + \
                                    '. ' + abstractDict['journal']
        abstractDict['publisher'] = '\\url{' + abstractDict['url'] + '}'
        return abstractDict


def getAbstractUrl(year, abstractNumber):
    BASEURL = 'http://archive.ismrm.org/'
    abstractNumberStr = str(abstractNumber)
    abstractNumberStr = (4 - len(abstractNumberStr)) * '0' + abstractNumberStr
    return BASEURL + str(year) + '/' + abstractNumberStr + '.html'


def getBibtexStrFromAbstractDict(abstractDict):
    abstractDict.pop('url')
    abstractDict.pop('journal')
    db = BibDatabase()
    writer = BibTexWriter()
    writer.indent = '    '
    db.entries = [abstractDict]
    return writer.write(db)


if __name__ == '__main__':
    main()
