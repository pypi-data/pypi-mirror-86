import click


@click.command()
def backup():
    print("Backing up!")


if __name__ == "__main__":
    backup()
