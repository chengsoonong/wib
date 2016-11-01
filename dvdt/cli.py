import subprocess
import click

class Repo(object):
    def __init__(self, vc_name='git'):
        self.vc_name = vc_name

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
def checkin(message, tag=None):
    """Commit saved changes to the repository.
    message - commit message
    """
    pass

@main.command()
def checkout(file_names):
    """Revert each file in the list file_names back to version in repo"""
    pass

@main.command()
def upload():
    """Synchronise local repo to remote repo"""
    pass

@main.command()
def download():
    """Synchronise remote repo to local repo"""
    pass

@main.command()
def status():
    """See which files have changed, checked in, and uploaded"""
    subprocess.call('git status', shell=True)

@main.command()
def log():
    """See history"""
    pass

@main.command()
def diff(file_name):
    """See changes that occured since last check in"""
    pass

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
