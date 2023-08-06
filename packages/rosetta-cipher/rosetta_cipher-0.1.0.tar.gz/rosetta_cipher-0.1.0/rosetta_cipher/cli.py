import click
from rosetta_cipher import cipher


@click.group()
@click.version_option(cipher.get_version())
def process():
    """Generate version names that are human readables"""
    pass


@process.command()
@click.option('--length', '-l', default=2)
@click.option('--retry', '-r', default=0)
@click.option('--separator', '-s', default='_', help='Separator')
@click.option('--capitalize', '-c', default=False, help='capitalize or not')
def random(length, retry, separator, capitalize):
    print(cipher.get_random_name(length, retry, separator, capitalize))


@process.command()
@click.argument('obj', default="")
@click.option('--length', '-l', default=2)
@click.option('--retry', '-r', default=0)
@click.option('--separator', '-s', default='_', help='Separator')
@click.option('--capitalize', '-c', default=False, help='capitalize or not')
def name(obj, length, retry, separator, capitalize):
    print(cipher.get_name(obj, length, retry, separator, capitalize))


if __name__ == '__main__':
    process()
