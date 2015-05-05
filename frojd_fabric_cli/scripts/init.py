import click
from frojd_fabric_cli import generator


@click.command()
@click.option("--stages", default="stage,prod")
@click.option("--path", default="./")
def main(stages, path):
    stage_list = stages.split(u",")
    stage_list = map(unicode.strip, stage_list)
    stage_list = filter(None, stage_list)

    formatted_stages = []

    for stage in stage_list:
        formatted_stages.append({
            "NAME": stage
        })

    gen = generator.Generator(stages=formatted_stages, path=path)
    gen.create_stages()

    click.echo(stage_list)
    click.echo(path)
