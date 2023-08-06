import click
import odakb
import subprocess
import yaml

def read_metadata():
    try:
        oda_meta_data = yaml.load(open("oda.yaml").read(), Loader=yaml.SafeLoader)
    except IOError:
        oda_meta_data = {}
        click.echo("not found!")

    return oda_meta_data

@click.group()
def cli():
    pass

def discover_directory_remote():
    git_remote = subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()

    return git_remote

@cli.command()
def up():
    oda_meta_data = read_metadata()

    remote = discover_directory_remote()
    click.echo(f"remote: {remote}")

    name = None
    if 'github.com' in remote:
        name = remote.split("/")[-1][:-4]

    odakb.sparql.insert(f"oda:{name} a oda:doc; oda:location \"{remote}\"")

    for tag in oda_meta_data.get('tags', []):
        c=f"oda:{name} oda:domain \"{tag}\""
        click.echo(c)
        odakb.sparql.insert(c)


@cli.command()
@click.option("-t", "--tag", default=None)
def tag(tag):
    oda_meta_data = read_metadata()

    if tag is not None:
        click.echo(f"tagging {tag}")
        oda_meta_data['tags'] = list(set(oda_meta_data.get('tags', []) + [tag]))

    yaml.dump(oda_meta_data, open("oda.yaml", "w"))


if __name__ == "__main__":
    cli()
