# -*- coding: utf-8 -*-

import sys
import argparse

import docutils.nodes
import docutils.parsers.rst
import docutils.utils

class MyVisitor(docutils.nodes.NodeVisitor):
    def visit_reference(self, node: docutils.nodes.enumerated_list):
        children = []
        for child in node.children:
            print(child)

    def unknow_visit(self, node: docutils.nodes.Node):
        pass

def create_anki_file_from_rst(inputFile):
    default_settings = docutils.frontend.OptionParser(
            components = (docutils.parsers.rst.Parser,)).get_default_values()
    document = docutils.utils.new_document(inputFile.name, default_settings)
    parser = docutils.parsers.rst.Parser()
    parser.parse(inputFile.read(), document)

    visitor = MyVisitor(document)
    document.walk(visitor)


def get_input_file_name():
    args = sys.argv
    if len(args) == 1:
        print('Please input English Sentence file name')
    elif len(args) == 2:
        return args[1]
    else:
        print('Too many arguments')

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputFile', nargs='?', type=argparse.FileType('r'),
                           default=sys.stdin)
    args = argparser.parse_args()
    print('Reading', args.inputFile.name)
    create_anki_file_from_rst(args.inputFile)

if __name__ == '__main__':
    main()
