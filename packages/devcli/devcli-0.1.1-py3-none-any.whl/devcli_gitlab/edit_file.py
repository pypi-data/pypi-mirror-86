import importlib

import click
from gitlab import GitlabGetError

from devcli_gitlab import GitlabClient
from devcli_gitlab.gitlab_group import gitlab


@gitlab.command()
@click.option('--group')
@click.option('--name')
@click.argument('--script', type=click.Path(exists=True))
@click.argument('--message', type=click.Path(exists=True))
@click.pass_obj
def edit_file(client: GitlabClient, group, name, script, message):

    client.do_for_every_project(group, edit_file_function(name, script, message))


def edit_file_function(file_name, script, message):

    spec = importlib.util.spec_from_file_location("edit_script", file_name.abolute())
    edit_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(edit_script)


    def edit_file(project):
        try:
            f = project.files.get(file_path=file_name, ref='master')
            edit_script.edit_file(project, file_name)
            f.save(branch='master', message=message)
        except GitlabGetError as e:
            print(e)
            if e.response_code == 404:
                print('file not in repo ,continuing')
                pass
            else:
                raise e

    return edit_file

