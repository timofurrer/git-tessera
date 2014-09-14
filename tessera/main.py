#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import os
import sys

from tesserae import Tesserae
from tesseraexceptions import TesseraError

pass_tesserae = click.make_pass_decorator(Tesserae)

@click.group()
@click.version_option("0.00.01")
@click.pass_context
def cli(ctx):
    """
        git tessera: the most simple git based tracking system
    """
    ctx.obj = Tesserae(os.getcwd())

@cli.command()
@pass_tesserae
def init(tesserae):
    """
        Initialize empty git tessera repository
    """
    try:
        return tesserae.init()
    except TesseraError, e:
        sys.stderr.write("Error: %s\n" % str(e))
        return False

@cli.command()
@click.argument("title", nargs=1, type=str)
@pass_tesserae
def create(tesserae, title):
    """
        Creates a new tessera.
    """
    try:
        return tesserae.create(title)
    except TesseraError, e:
        sys.stderr.write("Error: %s\n" % str(e))
        return False

@cli.command()
@click.argument("tessera_id")
@pass_tesserae
def rm(tesserae, tessera_id):
    """
        Removes a tessera by it's id.
    """
    try:
        return tesserae.remove(tessera_id)
    except TesseraError, e:
        sys.stderr.write("Error: %s\n" % str(e))
        return False

@cli.command()
@click.option("--order-by", type=str, default="priority", help="keyword to order by")
@click.option("--order-type", type=click.Choice(["asc", "desc"]), default="asc", help="order type. Ascending or Descending")
@click.option("--filter-types", type=str, help="filters for specific types")
@pass_tesserae
def ls(tesserae, order_by, order_type, filter_types):
    """
        List all existing tesserae
    """
    try:
        return tesserae.ls(order_by, order_type, set([x.strip() for x in filter_types.split(",")]) if filter_types else set())
    except TesseraError, e:
        sys.stderr.write("Error: %s\n" % str(e))
        return False

@cli.command()
@click.argument("tessera_id")
@pass_tesserae
def show(tesserae, tessera_id):
    """
        Show a specific tessera
    """
    try:
        return tesserae.show(tessera_id)
    except TesseraError, e:
        sys.stderr.write("Error: %s\n" % str(e))
        return False


if __name__ == "__main__":
    cli()
