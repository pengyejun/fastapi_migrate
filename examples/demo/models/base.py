import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


metadata = sqlalchemy.MetaData()

Model = declarative_base(metadata=metadata)
