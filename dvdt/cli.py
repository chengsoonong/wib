import subprocess
import click

class Repo(object):
    def __init__(self, debug, vc_name='git'):
        self.debug = debug
        self.vc_name = vc_name

    def shell(self, command):
        if self.debug:
            click.echo(command)
            to_cont = input('Continue? [y/n]')
            if to_cont != 'y':
                return
        subprocess.call(command, shell=True)


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True, default=False)
def main(context, debug):
    context.obj = Repo(debug)

@main.command()
@click.argument('repo_name')
@click.pass_context
def init(context, repo_name):
    """Start a new repository"""
    context.obj.shell('git init ' + repo_name)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def track(context, file_names):
    """Keep track of each file in list file_names.

    TODO: git ls-tree -r HEAD --name-only
    """
    for fn in file_names:
        context.obj.shell('git add ' + fn)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def untrack(context, file_names):
    """Forget about tracking each file in the list file_names"""
    for fn in file_names:
        context.obj.shell('git rm --cached ' + fn)

@main.command()
@click.argument('message')
@click.option('--name', default='')
@click.pass_context
def checkin(context, message, name):
    """Commit saved changes to the repository.
    message - commit message
    name    - tag name
    """
    context.obj.shell('git commit -a -m "' + message + '"')
    if name != '':
        context.obj.shell('git tag -a ' + name + ' -m "' + message + '"')

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def checkout(context, file_names):
    """Revert each file in the list file_names back to version in repo"""
    if len(file_names) == 0:
        click.echo('No file names to checkout specified.')
        click.echo('The following have changed since the last check in.')
        context.obj.shell('git status')
    for fn in file_names:
        context.obj.shell('git checkout -- ' + fn)

@main.command()
@click.option('--tags', is_flag=True, default=False)
@click.pass_context
def upload(context, tags):
    """Synchronise local repo to remote repo"""
    if tags:
        context.obj.shell('git push --tags')
    else:
        context.obj.shell('git push')

@main.command()
@click.pass_context
def download(context):
    """Synchronise remote repo to local repo"""
    context.obj.shell('git pull')

@main.command()
@click.pass_context
def status(context):
    """See which files have changed, checked in, and uploaded"""
    context.obj.shell('git status')

@main.command()
@click.pass_context
def log(context):
    """See history"""
    format = "'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
    context.obj.shell('git log --graph --pretty=format:' + format + ' --abbrev-commit --stat')

@main.command()
@click.argument('file_name', default='')
@click.pass_context
def diff(context, file_name):
    """See changes that occured since last check in"""
    context.obj.shell('git diff --color-words --ignore-space-change ' + file_name)

main.add_command(init)
main.add_command(track)
main.add_command(untrack)
main.add_command(checkin)
main.add_command(checkout)
main.add_command(upload)
main.add_command(download)
main.add_command(status)
main.add_command(log)
main.add_command(diff)
