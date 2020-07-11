import argparse
import os

from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from fastapi_migrate.command import Config

current_app = None


class Migrate:
    def __init__(self, app: FastAPI = None, model=None, directory: str = 'migrations', db_uri: str = None, **kwargs):
        self.configure_callbacks = []
        self.model = model
        self.directory = directory
        self.alembic_ctx_kwargs = kwargs
        if app is not None and model is not None and db_uri is not None:
            self.init_app(app, model, directory, db_uri)

    def init_app(self, app: FastAPI, model=None, directory: str = None, db_uri: str = None, **kwargs):
        self.model = model or self.model
        self.directory = directory or self.directory
        sqlalchemy_binds = self.alembic_ctx_kwargs.pop("SQLALCHEMY_BINDS", None) or kwargs.pop("SQLALCHEMY_BINDS", {})
        self.alembic_ctx_kwargs.update(kwargs)
        if not hasattr(app, 'extra'):
            app.extra = {}
        app.extra['migrate'] = _MigrateConfig(self, self.model, db_uri, sqlalchemy_binds, **self.alembic_ctx_kwargs)
        global current_app
        current_app = app

    def configure(self, f):
        self.configure_callbacks.append(f)
        return f

    def call_configure_callbacks(self, config):
        for f in self.configure_callbacks:
            config = f(config)
        return config

    def get_config(self, directory=None, x_arg=None, opts=None):
        if directory is None:
            directory = self.directory
        config = Config(os.path.join(directory, 'alembic.ini'))
        config.set_main_option('script_location', directory)
        if config.cmd_opts is None:
            config.cmd_opts = argparse.Namespace()
        for opt in opts or []:
            setattr(config.cmd_opts, opt, True)
        if not hasattr(config.cmd_opts, 'x'):
            if x_arg is not None:
                setattr(config.cmd_opts, 'x', [])
                if isinstance(x_arg, list) or isinstance(x_arg, tuple):
                    for x in x_arg:
                        config.cmd_opts.x.append(x)
                else:
                    config.cmd_opts.x.append(x_arg)
            else:
                setattr(config.cmd_opts, 'x', None)
        return self.call_configure_callbacks(config)


class _MigrateConfig(object):
    def __init__(self, migrate, model, db_uri, sqlalchemy_binds, **kwargs):
        self.migrate = migrate
        self.model = model
        self.db_uri = db_uri
        self.sqlalchemy_binds = sqlalchemy_binds
        self.directory = migrate.directory
        self.configure_args = kwargs

    @property
    def metadata(self):
        """
        Backwards compatibility, in old releases app.extensions['migrate']
        was set to db, and env.py accessed app.extensions['migrate'].metadata
        """
        return self.model.metadata
