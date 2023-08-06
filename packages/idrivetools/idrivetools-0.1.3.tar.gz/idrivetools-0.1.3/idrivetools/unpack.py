import click
"""
Take a folder containing a BMW backup and unpack it into a regular music folder
"""


@click.command()
@click.argument("source", type=click.Path(exists=True), default=".")
@click.argument("destination", default="restore")
def unpack_files(source, destination):
    print("Unpacking!")


if __name__ == "__main__":
    unpack_files()
