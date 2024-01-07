# -*- coding: utf-8 -*-
import sys
import argparse
import json

import docutils.nodes
import docutils.parsers.rst
import docutils.utils

class MyVisitor(docutils.nodes.GenericNodeVisitor):
    def __init__(self, document: docutils.nodes.document) -> None:
        super().__init__(document)
        self.notes = []
    def visit_list_item(self, node):
        record = {}
        sentence = node.astext()
        index = node[0].first_child_matching_class(docutils.nodes.strong)
        expression = ''
        if index is not None:
            expression = node[0][index].astext()
        record['expression'] = expression
        record['sentence'] = sentence
        self.notes.append(record)
    def default_visit(self, node):
        pass

def write_list_item_to_anki_file(items):
    with open('test.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(items, sort_keys=True, indent=4))

def create_anki_file_from_rst(fileobj):
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)).get_default_values()
    document = docutils.utils.new_document(fileobj.name, default_settings)
    parser = docutils.parsers.rst.Parser()
    parser.parse(fileobj.read(), document)
    visitor = MyVisitor(document)
    document.walk(visitor)
    write_list_item_to_anki_file(visitor.notes)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = argparser.parse_args()
    print('Reading ', args.infile.name)
    create_anki_file_from_rst(args.infile)

if __name__ == '__main__':
    main()
