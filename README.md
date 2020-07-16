Fastapi-Migrate
===============
fastapi-Migrate is an extension that handles SQLAlchemy database migrations for fastapi applications using Alembic. 

Tips:
-----
Since fastapi does not provide a command line similar to flask, you need to integrate the command line yourself. [How to use](./examples)

Usage:
Similar to flask_migrate

python [your_command](./examples/cli.py) db --help

python [your_command](./examples/cli.py) db init

python [your_command](./examples/cli.py) db migrate

python [your_command](./examples/cli.py) db upgrade


# Installing
pip install fastapi_migrate
