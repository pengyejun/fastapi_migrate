import click
from fastapi_migrate.cli import db
from demo.app import app
# 导入app


@click.group()
def cli():
    pass


@cli.command()
@click.option("-n", "--num", default=None, help='test command)')
def test(num):
    print(num)


cli.add_command(db)


if __name__ == "__main__":
    cli()
