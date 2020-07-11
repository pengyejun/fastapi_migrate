from pathlib import Path

from fastapi import FastAPI
from fastapi_migrate import Migrate

from .models import Model

CUR_PATH = Path(".").parent

app = FastAPI()
# 将app注入到fastapi_migrate
Migrate(app, model=Model, db_uri=f"sqlite:///{CUR_PATH / 'test.db'}")
