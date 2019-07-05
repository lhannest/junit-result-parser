import click

from html.parser import HTMLParser
from collections import defaultdict
from enum import Enum, auto

@click.command()
@click.option('-i', type=click.Path(exists=True), required=True)
@click.option('-o', type=click.Path(exists=False), required=True)
@click.option('--delineator', type=str, default='\n')
def duplicates(i, o, delineator):
    """
    Takes the results of parser and outputs a list of duplicates
    """
    with click.open_file(i, 'r') as f_in:
        tests = f_in.read().split(delineator)

        duplicates = set()

        while len(tests) > 0:
            test = tests.pop(0)
            if test in tests:
                duplicates.add(test)

        duplicates = list(duplicates)
        duplicates.sort()

        with click.open_file(o, 'w+') as f_out:
            f_out.write('\n'.join(duplicates))

if __name__ == '__main__':
    duplicates()
