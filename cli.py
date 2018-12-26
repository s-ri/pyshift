#!/usr/bin/env python3
# coding: utf-8

import click
from pyshift.commands import ShiftCommand

cli = click.CommandCollection(sources=[ShiftCommand])

if __name__ == '__main__':
    cli()
