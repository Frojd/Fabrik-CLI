import click
from frojd_fabric_cli import generator
from frojd_fabric_cli import utils


@click.command()
@click.option("--stages", default="stage,prod")
@click.option("--path", default="./")
def main(stages, path):
    stage_list = stages.split(u",")
    stage_list = map(unicode.strip, stage_list)
    stage_list = filter(None, stage_list)

    formatted_stages = []

    config = {}
    params = {}

    for stage in stage_list:
        formatted_stages.append({
            "NAME": stage
        })

    if utils.has_git_repro(path):
        repro_url = utils.get_git_remote(path)
        repro_url = click.prompt("git repository", default=repro_url)

        config["git"] = True
        params["repro_url"] = repro_url

    gen = generator.Generator(stages=formatted_stages, path=path,
                              config=config, params=params)
    gen.create_index()
    gen.create_stages()

    #click.echo(stage_list)
    #click.echo(path)