## Installation:
0 - Copy example.env to .env
``` bash
cp example.env .env
```

1 - Install pipenv
```
pip install pipenv
```

2 - Activate the virtual environment
```
pipenv shell
```

3 - Install the dependencies
```
pipenv install
```

4 - Create the database:
Download and install docker if necessary. Then run the following command:
```
docker-compose up
```
Use the `-d` flag to run in detached mode (optional).

5 - Run the application
```
 uvicorn app.api.main:app --reload 
 ```


## Migrations
### Creating a new Model

1 - Create the model in a separate file at `app/models` directory. This module contains the models for the database. 
For schemas or stateless models refer to the `app/schemas` directory.
To register a database model it must be imported in the `app/models/__init__.py` file. This will cause Alembic to register the model for migrations.

2 - Create a new migration
After the model is created and registered, a new migration can be created by running the following command:
```
alembic revision --autogenerate -m "Your message here"
```
Be descriptive and consistent with the message. This will create a new migration file in the `alembic/versions` directory.

3 - Apply the migration
After the migration is created, it can be applied to the database by running the following command:
```
alembic upgrade head
```

