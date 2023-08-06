"""Console script for freud_api_crawler."""
import os
import sys
import click

from . import freud_api_crawler as frd


@click.command()
@click.argument('user', envvar='FRD_USER')
@click.argument('pw', envvar='FRD_PW')
@click.argument('session', envvar='FRD_SESSION')
@click.argument('token', envvar='FRD_TOKEN')
@click.option('-m', default='a10e8c78-adad-4ca2-bfcb-b51bedcd7b58', show_default=True)
def cli(user, pw, session, token, m):
    """Console script for freud_api_crawler."""
    frd_manifestation = frd.FrdManifestation(
        user=user,
        pw=pw,
        session=session,
        token=token,
        manifestation_id=m
    )
    xml = frd_manifestation.make_xml(save=True)
    click.echo(
        click.style(
            f"processed Manifestation\n###\n {frd_manifestation.md__title}\
            {frd_manifestation.manifestation_id}\n###", fg='green'
        )
    )


@click.command()
@click.argument('user', envvar='FRD_USER')
@click.argument('pw', envvar='FRD_PW')
@click.argument('session', envvar='FRD_SESSION')
@click.argument('token', envvar='FRD_TOKEN')
@click.option('-m', default='a10e8c78-adad-4ca2-bfcb-b51bedcd7b58', show_default=True)
@click.option('-s', default='/freud_data', show_default=True)
def save_test(user, pw, session, token, m, s):
    """Console script for freud_api_crawler."""
    # frd_manifestation = frd.FrdManifestation(
    #     user=user,
    #     pw=pw,
    #     session=session,
    #     token=token,
    #     manifestation_id=m,
    # )
    cur_loc = os.path.dirname(os.path.abspath(__file__))
    # xml = frd_manifestation.make_xml(save=True)
    click.echo(
        f"cur_loc: {cur_loc}"
    )
    click.echo(
        f"save_dir: {s}"
    )
