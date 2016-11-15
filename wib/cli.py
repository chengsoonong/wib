import subprocess
import sys
import click

class Repo(object):
    def __init__(self, debug, vc_name='git'):
        self.debug = debug
        self.vc_name = vc_name

    def shell(self, command):
        if self.debug:
            click.echo(command)
            click.confirm('Continue?', default=True, abort=True)
        try:
            ret_code = subprocess.call(command, shell=True)
        except subprocess.CalledProcessError:
            return False
        return ret_code



@click.group()
@click.pass_context
@click.option('--debug', is_flag=True, default=False)
def main(context, debug):
    context.obj = Repo(debug)
    is_git = context.obj.shell('git rev-parse --is-inside-work-tree')
    if is_git != 0:
        print('not git')
        is_hg = context.obj.shell('hg -q stat 2> /dev/null > /dev/null')
        if is_hg != 0:
            print('not hg')
            exit(1)
        else:
            context.obj.vc_name = 'hg'


@main.command()
@click.argument('repo_name')
@click.pass_context
def init(context, repo_name):
    """Start a new repository"""
    context.obj.shell(context.obj.vc_name + ' init ' + repo_name)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def track(context, file_names):
    """Keep track of each file in list file_names."""
    for fn in file_names:
        context.obj.shell(context.obj.vc_name + ' add ' + fn)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def untrack(context, file_names):
    """Forget about tracking each file in the list file_names"""
    for fn in file_names:
        if context.obj.vc_name == 'git':
            context.obj.shell('git rm --cached ' + fn)
        elif context.obj.vc_name == 'hg':
            context.obj.shell('hg forget ' + fn)

@main.command()
@click.argument('message')
@click.option('--name', default='')
@click.pass_context
def checkin(context, message, name):
    """Commit saved changes to the repository.
    message - commit message
    name    - tag name
    """
    if context.obj.vc_name == 'git':
        context.obj.shell('git commit -a -m "' + message + '"')
    elif context.obj.vc_name == 'hg':
        context.obj.shell('hg commit -m "' + message + '"')
    if name != '' and context.obj.vc_name == 'git':
        context.obj.shell('git tag -a ' + name + ' -m "' + message + '"')
    elif name != '' and context.obj.vc_name == 'hg':
        context.obj.shell('hg tag -m "' + message + '" ' + name)

@main.command()
@click.argument('message')
@click.option('--name', default='')
@click.pass_context
def ci(context, message, name):
    """alias for checkin"""
    context.forward(checkin)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def checkout(context, file_names):
    """Revert each file in the list file_names back to version in repo"""
    if len(file_names) == 0:
        click.echo('No file names to checkout specified.')
        click.echo('The following have changed since the last check in.')
        context.invoke(status)
    for fn in file_names:
        if context.obj.vc_name == 'git':
            context.obj.shell('git checkout -- ' + fn)
        elif context.obj.vc_name == 'hg':
            context.obj.shell('hg revert --no-backup ' + fn)

@main.command()
@click.argument('file_names', nargs=-1)
@click.pass_context
def co(context, file_names):
    """"alias for checkout"""
    context.forward(checkout)

@main.command()
@click.pass_context
def upload(context):
    """Synchronise local repo to remote repo"""
    if context.obj.vc_name == 'git':
        context.obj.shell('git push')
        context.obj.shell('git push --tags')
    elif context.obj.vc_name == 'hg':
        context.obj.shell('hg push')

@main.command()
@click.pass_context
def up(context):
    """alias for upload"""
    context.forward(upload)

@main.command()
@click.argument('repo_url', nargs=1, default='')
@click.pass_context
def download(context, repo_url):
    """Synchronise remote repo to local repo.

    If repo_url is given, then clone from remote URL.
    """
    if repo_url == '':
        if context.obj.vc_name == 'git':
            context.obj.shell('git pull')
        elif context.obj.vc_name == 'hg':
            context.obj.shell('hg pull -u')
    else:
        context.obj.shell(context.obj.vc_name + ' clone ' + repo_url)


@main.command()
@click.argument('repo_url', nargs=1, default='')
@click.pass_context
def down(context, repo_url):
    """alias for download"""
    context.forward(download)

@main.command()
@click.pass_context
def status(context):
    """See which files have changed, checked in, and uploaded"""
    context.obj.shell(context.obj.vc_name + ' status')

@main.command()
@click.pass_context
def log(context):
    """See history"""
    if context.obj.vc_name == 'git':
        format = "'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
        context.obj.shell('git log --graph --pretty=format:' + format + ' --abbrev-commit --stat')
    elif context.obj.vc_name == 'hg':
        context.obj.shell('hg log -G --template changeset:   {rev}:{node|short} {tags}\nsummary:     {desc|firstline|fill68|tabindent|tabindent}')

@main.command()
@click.argument('file_name', default='')
@click.pass_context
def diff(context, file_name):
    """See changes that occured since last check in"""
    if context.obj.vc_name == 'git':
        context.obj.shell('git diff --color-words --ignore-space-change ' + file_name)
    elif context.obj.vc_name == 'hg':
        context.obj.shell('hg diff ' + file_name)

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
