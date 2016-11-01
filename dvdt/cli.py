import subprocess
import click

class Repo(object):
    def __init__(self, vc_name='git'):
        self.vc_name = vc_name

def _shell(command, debug=True):
    if debug:
        click.echo(command)
        to_cont = input('Continue? [y/n]')
        if to_cont != 'y':
            return
    subprocess.call(command, shell=True)

@click.group()
@click.pass_context
def main(context):
    context.obj = Repo()

@main.command()
def init():
    """Start a new repository"""
    pass

@main.command()
def track(file_names):
    """Keep track of each file in list file_names"""
    pass

@main.command()
def untrack(file_names):
    """Forget about tracking each file in the list file_names"""
    pass

@main.command()
@click.argument('message')
@click.option('--name', default='')
def checkin(message, name):
    """Commit saved changes to the repository.
    message - commit message
    name    - tag name
    """
    _shell('git commit -a -m "' + message + '"')
    if name != '':
        _shell('git tag -a ' + name + ' -m "' + message + '"')

@main.command()
@click.argument('file_names', nargs=-1)
def checkout(file_names):
    """Revert each file in the list file_names back to version in repo"""
    if len(file_names) == 0:
        click.echo('No file names to checkout specified.')
        click.echo('The following have changed since the last check in.')
        _shell('git status')
    for fn in file_names:
        _shell('git checkout -- ' + fn)

@main.command()
@click.option('--tags', is_flag=True, default=False)
def upload(tags):
    """Synchronise local repo to remote repo"""
    if tags:
        _shell('git push --tags')
    else:
        _shell('git push')

@main.command()
def download():
    """Synchronise remote repo to local repo"""
    _shell('git pull')

@main.command()
def status():
    """See which files have changed, checked in, and uploaded"""
    _shell('git status')

@main.command()
def log():
    """See history"""
    format = "'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
    _shell('git log --graph --pretty=format:' + format + ' --abbrev-commit --stat')

@main.command()
@click.argument('file_name', default='')
def diff(file_name):
    """See changes that occured since last check in"""
    _shell('git diff --color-words --ignore-space-change ' + file_name)

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
