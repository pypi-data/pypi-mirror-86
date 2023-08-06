import logging

from kouyierr import index
from kouyierr.commands import invoice


def main() -> None:
    logging.basicConfig(format='%(message)s')
    logging.getLogger(__package__).setLevel(logging.INFO)
    invoice.register()
    index.register()
    index.index()
