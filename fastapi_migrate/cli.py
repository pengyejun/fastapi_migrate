import click

from .command import init as _init
from .command import revision as _revision
from .command import migrate as _migrate
from .command import edit as _edit
from .command import merge as _merge
from .command import upgrade as _upgrade
from .command import downgrade as _downgrade
from .command import show as _show
from .command import history as _history
from .command import heads as _heads
from .command import branches as _branches
from .command import current as _current
from .command import stamp as _stamp


@click.group()
def db():
    pass


@db.command()
@click.option("-d", "--direct", default=None,
              help='migration script directory (default is "migrations")')
def init(direct):
    _init(direct)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-m', '--message', default=None, help='Revision message')
@click.option('--autogenerate', is_flag=True,
              help='Populate revision script with candidate migration '
              'operations, based on comparison of database to model')
@click.option('--sql', is_flag=True,
              help='Don\'t emit SQL to database - dump to standard output '
              'instead')
@click.option('--head', default='head',
              help='Specify head revision or <branchname>@head to base new '
              'revision on')
@click.option('--splice', is_flag=True,
              help='Allow a non-head revision as the "head" to splice onto')
@click.option('--branch-label', default=None,
              help='Specify a branch label to apply to the new revision')
@click.option('--version-path', default=None,
              help='Specify specific path from config for version file')
@click.option('--rev-id', default=None,
              help='Specify a hardcoded revision id instead of generating '
              'one')
def revision(directory, message, autogenerate, sql, head, splice, branch_label,
             version_path, rev_id):
    """Create a new revision file."""
    _revision(directory, message, autogenerate, sql, head, splice,
              branch_label, version_path, rev_id)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-m', '--message', default=None, help='Revision message')
@click.option('--sql', is_flag=True,
              help='Don\'t emit SQL to database - dump to standard output '
              'instead')
@click.option('--head', default='head',
              help='Specify head revision or <branchname>@head to base new '
              'revision on')
@click.option('--splice', is_flag=True,
              help='Allow a non-head revision as the "head" to splice onto')
@click.option('--branch-label', default=None,
              help='Specify a branch label to apply to the new revision')
@click.option('--version-path', default=None,
              help='Specify specific path from config for version file')
@click.option('--rev-id', default=None,
              help='Specify a hardcoded revision id instead of generating '
              'one')
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
def migrate(directory, message, sql, head, splice, branch_label, version_path,
            rev_id, x_arg):
    """Autogenerate a new revision file (Alias for 'revision --autogenerate')"""
    _migrate(directory, message, sql, head, splice, branch_label, version_path,
             rev_id, x_arg)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.argument('revision', default='head')
def edit(directory, revision):
    """Edit a revision file"""
    _edit(directory, revision)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-m', '--message', default=None, help='Merge revision message')
@click.option('--branch-label', default=None,
              help='Specify a branch label to apply to the new revision')
@click.option('--rev-id', default=None,
              help='Specify a hardcoded revision id instead of generating '
              'one')
@click.argument('revisions', nargs=-1)
def merge(directory, message, branch_label, rev_id, revisions):
    """Merge two revisions together, creating a new revision file"""
    _merge(directory, revisions, message, branch_label, rev_id)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('--sql', is_flag=True,
              help='Don\'t emit SQL to database - dump to standard output '
              'instead')
@click.option('--tag', default=None,
              help='Arbitrary "tag" name - can be used by custom "env.py '
              'scripts')
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
@click.argument('revision', default='head')
def upgrade(directory, sql, tag, x_arg, revision):
    """Upgrade to a later version"""
    _upgrade(directory, revision, sql, tag, x_arg)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('--sql', is_flag=True,
              help=('Don\'t emit SQL to database - dump to standard output '
                    'instead'))
@click.option('--tag', default=None,
              help=('Arbitrary "tag" name - can be used by custom "env.py '
                    'scripts'))
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
@click.argument('revision', default='-1')
def downgrade(directory, sql, tag, x_arg, revision):
    """Revert to a previous version"""
    _downgrade(directory, revision, sql, tag, x_arg)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.argument('revision', default='head')
def show(directory, revision):
    """Show the revision denoted by the given symbol."""
    _show(directory, revision)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-r', '--rev-range', default=None,
              help='Specify a revision range; format is [start]:[end]')
@click.option('-v', '--verbose', is_flag=True, help='Use more verbose output')
@click.option('-i', '--indicate-current', is_flag=True,
              help='Indicate current version (Alembic 0.9.9 or greater is required)')
def history(directory, rev_range, verbose, indicate_current):
    """List changeset scripts in chronological order."""
    _history(directory, rev_range, verbose, indicate_current)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-v', '--verbose', is_flag=True, help='Use more verbose output')
@click.option('--resolve-dependencies', is_flag=True,
              help='Treat dependency versions as down revisions')
def heads(directory, verbose, resolve_dependencies):
    """Show current available heads in the script directory"""
    _heads(directory, verbose, resolve_dependencies)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-v', '--verbose', is_flag=True, help='Use more verbose output')
def branches(directory, verbose):
    """Show current branch points"""
    _branches(directory, verbose)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('-v', '--verbose', is_flag=True, help='Use more verbose output')
@click.option('--head-only', is_flag=True,
              help='Deprecated. Use --verbose for additional output')
def current(directory, verbose, head_only):
    """Display the current revision for each database."""
    _current(directory, verbose, head_only)


@db.command()
@click.option('-d', '--directory', default=None,
              help='migration script directory (default is "migrations")')
@click.option('--sql', is_flag=True,
              help='Don\'t emit SQL to database - dump to standard output '
              'instead')
@click.option('--tag', default=None,
              help='Arbitrary "tag" name - can be used by custom "env.py '
              'scripts')
@click.argument('revision', default='head')
def stamp(directory, sql, tag, revision):
    """'stamp' the revision table with the given revision; don't run any
    migrations"""
    _stamp(directory, revision, sql, tag)
