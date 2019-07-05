import click

from html.parser import HTMLParser
from collections import defaultdict
from enum import Enum, auto

@click.command()
@click.argument('first', type=click.Path(exists=True))
@click.argument('second', type=click.Path(exists=True))
@click.option('-o', type=click.Path(exists=False), required=True)
@click.option('--rm-duplicates', is_flag=True, help='If set will remove duplicate tests before saving')
@click.option('--delineator', type=str, default='\n')
def compare(first, second, o, rm_duplicates, delineator):
    """
    Outputs all tests contained in the first but not in the second
    """
    with click.open_file(first, 'r') as f_first:
        with click.open_file(second, 'r') as f_second:
            a = f_first.read().split(delineator)
            b = f_second.read().split(delineator)
            if rm_duplicates:
                a = set(a)
                b = set(b)

            c = [x for x in a if x not in b]
            c.sort()

            with click.open_file(o, 'w+') as f_out:
                f_out.write(delineator.join(c))

if __name__ == '__main__':
    compare()
