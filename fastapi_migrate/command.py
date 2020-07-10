import sys
import os
import logging
from pathlib import Path
from functools import wraps

import fastapi
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.util import CommandError
from alembic import __version__ as __alembic_version__


log = logging.getLogger()
alembic_version = tuple([int(v) for v in __alembic_version__.split('.')[0:3]])


class Config(AlembicConfig):
    def get_template_directory(self):
        package_dir = Path(__file__).parent
        return str((package_dir / "templates").absolute())


def catch_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (CommandError, RuntimeError) as exc:
            log.error('Error: ' + str(exc))
            sys.exit(1)
    return wrapped


def current_app() -> fastapi.FastAPI:
    from fastapi_migrate import current_app
    if not isinstance(current_app, fastapi.FastAPI):
        log.error(
            "No fastapi application running, Check if Migate(app) has been executed")
    return current_app


@catch_errors
def init(directory=None):
    """Creates a new migration repository"""
    app = current_app()
    if directory is None:
        directory = app.extra['migrate'].directory
    config = Config()
    config.set_main_option('script_location', directory)
    config.config_file_name = os.path.join(directory, 'alembic.ini')
    config = app.extra['migrate'].migrate.call_configure_callbacks(config)
    command.init(config, directory, 'fastapi')


@catch_errors
def revision(directory=None, message=None, autogenerate=False, sql=False,
             head='head', splice=False, branch_label=None, version_path=None,
             rev_id=None):
    """Create a new revision file."""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory)
    if alembic_version >= (0, 7, 0):
        command.revision(config, message, autogenerate=autogenerate, sql=sql,
                         head=head, splice=splice, branch_label=branch_label,
                         version_path=version_path, rev_id=rev_id)
    else:
        command.revision(config, message, autogenerate=autogenerate, sql=sql)


@catch_errors
def migrate(directory=None, message=None, sql=False, head='head', splice=False,
            branch_label=None, version_path=None, rev_id=None, x_arg=None):
    """Alias for 'revision --autogenerate'"""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(
        directory, opts=['autogenerate'], x_arg=x_arg)
    if alembic_version >= (0, 7, 0):
        command.revision(config, message, autogenerate=True, sql=sql,
                         head=head, splice=splice, branch_label=branch_label,
                         version_path=version_path, rev_id=rev_id)
    else:
        command.revision(config, message, autogenerate=True, sql=sql)


@catch_errors
def edit(directory=None, _revision='current'):
    """Edit current revision."""
    if alembic_version >= (0, 8, 0):
        app = current_app()
        config = app.extra['migrate'].migrate.get_config(
            directory)
        command.edit(config, _revision)
    else:
        raise RuntimeError('Alembic 0.8.0 or greater is required')


@catch_errors
def merge(directory=None, revisions='', message=None, branch_label=None,
          rev_id=None):
    """Merge two revisions together.  Creates a new migration file"""
    if alembic_version >= (0, 7, 0):
        app = current_app()
        config = app.extra['migrate'].migrate.get_config(
            directory)
        command.merge(config, revisions, message=message,
                      branch_label=branch_label, rev_id=rev_id)
    else:
        raise RuntimeError('Alembic 0.7.0 or greater is required')


@catch_errors
def upgrade(directory=None, _revision='head', sql=False, tag=None, x_arg=None):
    """Upgrade to a later version"""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory,
                                                     x_arg=x_arg)
    command.upgrade(config, _revision, sql=sql, tag=tag)


@catch_errors
def downgrade(directory=None, _revision='-1', sql=False, tag=None, x_arg=None):
    """Revert to a previous version"""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory,
                                                     x_arg=x_arg)
    if sql and _revision == '-1':
        _revision = 'head:-1'
    command.downgrade(config, _revision, sql=sql, tag=tag)


@catch_errors
def show(directory=None, _revision='head'):
    """Show the revision denoted by the given symbol."""
    if alembic_version >= (0, 7, 0):
        app = current_app()
        config = app.extra['migrate'].migrate.get_config(
            directory)
        command.show(config, _revision)
    else:
        raise RuntimeError('Alembic 0.7.0 or greater is required')


@catch_errors
def history(directory=None, rev_range=None, verbose=False, indicate_current=False):
    """List changeset scripts in chronological order."""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory)
    if alembic_version >= (0, 9, 9):
        command.history(config, rev_range, verbose=verbose,
                        indicate_current=indicate_current)
    elif alembic_version >= (0, 7, 0):
        command.history(config, rev_range, verbose=verbose)
    else:
        command.history(config, rev_range)


@catch_errors
def heads(directory=None, verbose=False, resolve_dependencies=False):
    """Show current available heads in the script directory"""
    if alembic_version >= (0, 7, 0):
        app = current_app()
        config = app.extra['migrate'].migrate.get_config(
            directory)
        command.heads(config, verbose=verbose,
                      resolve_dependencies=resolve_dependencies)
    else:
        raise RuntimeError('Alembic 0.7.0 or greater is required')


@catch_errors
def branches(directory=None, verbose=False):
    """Show current branch points"""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory)
    if alembic_version >= (0, 7, 0):
        command.branches(config, verbose=verbose)
    else:
        command.branches(config)


@catch_errors
def current(directory=None, verbose=False, head_only=False):
    """Display the current revision for each database."""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory)
    if alembic_version >= (0, 7, 0):
        command.current(config, verbose=verbose, head_only=head_only)
    else:
        command.current(config)


@catch_errors
def stamp(directory=None, _revision='head', sql=False, tag=None):
    """'stamp' the revision table with the given revision; don't run any
    migrations"""
    app = current_app()
    config = app.extra['migrate'].migrate.get_config(directory)
    command.stamp(config, _revision, sql=sql, tag=tag)
