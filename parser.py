import click

from html.parser import HTMLParser
from collections import defaultdict
from enum import Enum, auto

class JUnitTestParser(HTMLParser):
    mapping = defaultdict(list)
    tests = []
    suites = []
    li = None
    em = None
    span = None

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.li = attrs
        elif tag == 'em':
            self.em = attrs
        elif tag == 'span':
            self.span = attrs

    def handle_endtag(self, tag):
        if tag == 'li':
            self.li = None
        elif tag == 'em':
            self.em = None
        elif tag == 'span':
            self.span = None

    def handle_data(self, data):
        # If we're in <li> and in <span>, but not in <em>
        if self.li is not None and self.em is None and self.span is not None:
            for attr_name, v in self.li:
                if attr_name == 'class':
                    if 'top' in v or 'suite' in v:
                        self.suites.append(data)

                    if 'test' in v:
                        self.tests.append(data)
                        suite = self.suites[-1] if len(self.suites) > 0 else '<no suite>'
                        self.mapping[suite].append(data)

@click.command()
@click.option('-i', type=click.Path(exists=True), required=True)
@click.option('-o', type=click.Path(exists=False), required=True)
@click.option('--sort', is_flag=True, help='Sort the tests by their names before saving')
@click.option('--rm-duplicates', is_flag=True, help='Remove duplicate tests before saving')
@click.option('--delineator', type=str, default='\n')
def parse(i, o, sort, rm_duplicates, delineator):
    parser = JUnitTestParser()
    with click.open_file(i, 'r') as f_in:
        parser.feed(f_in.read())
        tests = parser.tests
        with click.open_file(o, 'w+') as f_out:
            if sort: tests.sort()
            if rm_duplicates: tests = list(set(tests))

            f_out.write(delineator.join(tests))

if __name__ == '__main__':
    parse()
