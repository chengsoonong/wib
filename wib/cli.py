import shutil
import subprocess
import os
import click


class Repo(object):
    def __init__(self, debug, vc_name='git'):
        self.debug = debug
        self.vc_name = vc_name
        self.FNULL = open(os.devnull, 'w')

    def call(self, args, devnull=False):
        """Call other processes.
        args - list of command args
        devnull - whether to pipe stdout to /dev/null (or equivalent)
        """
        if self.debug:
            click.echo(subprocess.list2cmdline(args))
            click.confirm('Continue?', default=True, abort=True)
        try:
            kwargs = {}
            if devnull:
                # Pipe to /dev/null (or equivalent).
                kwargs['stderr'] = subprocess.STDOUT
                kwargs['stdout'] = self.FNULL
            ret_code = subprocess.call(args, **kwargs)
        except subprocess.CalledProcessError:
            return False
        return ret_code

    def find_repo_type(self):
        """Check for git or hg repository"""
        is_git = self.call(['git', 'rev-parse', '--is-inside-work-tree'],
                           devnull=True)
        if is_git != 0:
            if self.debug:
                click.echo('not git')
            is_hg = self.call(['hg', '-q', 'stat'], devnull=True)
            if is_hg != 0:
                if self.debug:
                    click.echo('not hg')
                exit(1)
            else:
                self.vc_name = 'hg'


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True, default=False)
@click.version_option()
def main(context, debug):
    context.obj = Repo(debug)


@main.command()
@click.argument('file_names', nargs=-1, type=click.Path())
@click.pass_context
def track(context, file_names):
    """Keep track of each file in list file_names."""
    context.obj.find_repo_type()
    for fn in file_names:
        context.obj.call([context.obj.vc_name, 'add', fn])


@main.command()
@click.argument('file_names', nargs=-1, type=click.Path())
@click.pass_context
def untrack(context, file_names):
    """Forget about tracking each file in the list file_names"""
    context.obj.find_repo_type()
    for fn in file_names:
        if context.obj.vc_name == 'git':
            context.obj.call(['git', 'rm', '--cached ', fn])
        elif context.obj.vc_name == 'hg':
            context.obj.call(['hg', 'forget', fn])


@main.command()
@click.argument('message')
@click.option('--name', default='')
@click.pass_context
def commit(context, message, name):
    """Commit saved changes to the repository.
    message - commit message
    name    - tag name
    """
    context.obj.find_repo_type()
    if context.obj.vc_name == 'git':
        context.obj.call(['git', 'commit', '-a', '-m', message])
    elif context.obj.vc_name == 'hg':
        context.obj.call(['hg', 'commit', '-m', message])
    if name != '' and context.obj.vc_name == 'git':
        context.obj.call(['git', 'tag', '-a', name, '-m', message])
    elif name != '' and context.obj.vc_name == 'hg':
        context.obj.call(['hg', 'tag', '-m', message, name])


@main.command()
@click.argument('message')
@click.option('--name', default='')
@click.pass_context
def ci(context, message, name):
    """alias for commit"""
    context.forward(commit)


@main.command()
@click.argument('file_names', nargs=-1, type=click.Path())
@click.pass_context
def revert(context, file_names):
    """Revert each file in the list file_names back to version in repo"""
    context.obj.find_repo_type()
    if len(file_names) == 0:
        click.echo('No file names to checkout specified.')
        click.echo('The following have changed since the last check in.')
        context.invoke(status)
    for fn in file_names:
        if context.obj.vc_name == 'git':
            context.obj.call(['git', 'checkout', '--', fn])
        elif context.obj.vc_name == 'hg':
            context.obj.call(['hg', 'revert', '--no-backup', fn])


@main.command()
@click.pass_context
def up(context):
    """(upload) Synchronise local repo to remote repo"""
    context.obj.find_repo_type()
    if context.obj.vc_name == 'git':
        context.obj.call(['git', 'push'])
        context.obj.call(['git', 'push', '--tags'])
    elif context.obj.vc_name == 'hg':
        context.obj.call(['hg', 'push'])


@main.command()
@click.argument('repo_url', nargs=1, default='')
@click.pass_context
def down(context, repo_url):
    """(download) Synchronise remote repo to local repo.

    If repo_url is given, then clone from remote URL.
    """
    if repo_url == '':
        context.obj.find_repo_type()
        if context.obj.vc_name == 'git':
            context.obj.call(['git', 'pull'])
        elif context.obj.vc_name == 'hg':
            context.obj.call(['hg', 'pull', '-u'])
    else:
        context.obj.call([context.obj.vc_name, 'clone', repo_url])


@main.command()
@click.pass_context
def status(context):
    """See which files have changed, checked in, and uploaded"""
    context.obj.find_repo_type()
    context.obj.call([context.obj.vc_name, 'status'])


@main.command()
@click.pass_context
def log(context):
    """See history"""
    context.obj.find_repo_type()
    if context.obj.vc_name == 'git':
        format = ("--pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset "
                  "%s %Cgreen(%cr) %C(bold blue)<%an>%Creset'")
        context.obj.call(['git', 'log', '--graph', format,
                          '--abbrev-commit', '--stat'])
    elif context.obj.vc_name == 'hg':
        template = (
            '"changeset:   {rev}:{node|short} {tags}\n'
            ' summary:     {desc|firstline|fill68|tabindent|tabindent}"')
        context.obj.call(['hg', 'log', '-G', '--template', template])


@main.command()
@click.argument('file_name', default='')
@click.pass_context
def diff(context, file_name):
    """See changes that occured since last check in"""
    context.obj.find_repo_type()
    if context.obj.vc_name == 'git':
        context.obj.call(['git', 'diff', '--color-words',
                          '--ignore-space-change', file_name])
    elif context.obj.vc_name == 'hg':
        context.obj.call(['hg', 'diff', file_name])


main.add_command(track)
main.add_command(untrack)
main.add_command(commit)
main.add_command(revert)
main.add_command(up)
main.add_command(down)
main.add_command(status)
main.add_command(log)
main.add_command(diff)
