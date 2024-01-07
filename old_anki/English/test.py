# -*- coding: utf-8 -*-

import argparse
import sys

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
from pprint import pprint

class MyVisitor(docutils.nodes.GenericNodeVisitor):
    def visit_list_item(self, node):
        sentence = node[0]
        notes = node[1]
        for child in sentence.children:
            if child.tagname == 'strong':
                item = child.children[0]
                break

        item = item + '\t' + sentence.rawsource.replace('*', '').replace('\n', '')
        for child in notes.children:
            if child == notes.children[0]:
                item = item + '\t'
            else:
                item = item + '<br>'
            item = item + child.rawsource.replace('*', '').replace('\n', ' ')
        item += '\n'
        f(item)
        print(item)

    def default_visit(self, node):
        pass

def f(item, L=[]):
    L.append(item)
    return L

def write_list_item_to_anki_file(items):
    with open('test.csv', 'w+') as f:
        for item in items:
            f.write(item)

def create_anki_file_from_rst(fileobj):
    # Parse the file into a document with the rst parser.
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)).get_default_values()
    document = docutils.utils.new_document(fileobj.name, default_settings)
    parser = docutils.parsers.rst.Parser()
    parser.parse(fileobj.read(), document)

    # Visit the parsed document with our link-checking visitor.
    visitor = MyVisitor(document)
    document.walk(visitor)
    write_list_item_to_anki_file(f(""))


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                           default=sys.stdin)
    args = argparser.parse_args()
    if args.infile.name[-4:] != '.rst':
        print("Please input rst file!!!")
        return
    print('Reading', args.infile.name)
    create_anki_file_from_rst(args.infile)

if __name__ == '__main__':
    main()
