# Launch Historeno platform

## Setting up

- install docker and docker-compose
- create .env-db file based on .env-db-template
```
#placeholder for the env file
DB_HOST=host
DB_PORT=1234
DB_USER=user
DB_PASSWORD=password
DB_DB=databasename
```

## Commands

* build of the plateform (on Linux)
```bash
docker-compose up --build 
```
* integrate data in the database 
```bash
docker-compose --file docker-compose-db.yml up --build -d data-integration
```
* load layer (on Linux)
```bash
docker-compose exec api /bin/bash -c 'flask update-dataset 1'
```
* load layer (on Windows)
```bash
docker-compose exec api /bin/bash -c "flask update-dataset 1"
```


# CM Historeno
## Service name
- cm-historeno

# Database
## Service name 
- db

## Modification from EmerMaps
- added variable environment in the docker-compose
```yml
PGDATA: /var/lib/postgresql/data/historeno
```

## pgAdmin acess

```markdown
host : 127.0.0.1
Port : 5433
Maintenance database : postgres
Username : test (or see .env-db)
DB_PASSWORD : example (or see .env-db)
```

# Postgrest

## Modification from EmerMaps
1. generate the json web token, with this tutorial :
  - https://postgrest.org/en/stable/tutorials/tut1.html#tut1
  - https://jwt.io/#debugger-io

2. add .postgrest file
```
PGRST_DB_URI=postgres://test:example@db:5432/dataset
PGRST_DB_ANON_ROLE=api_anon
PGRST_JWT_SECRET=4yHaZ1QtEKmgpR7E295RSs6CdiWyWyjn48DXr3tcLAMawDew5MiFJJLMdDwbc6fi
```

3. Test with simple request
```python
import requests
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYXBpX3VzZXIifQ.II34IQz5jIqOnOoAKM7ou9eg8zOxnQqjHhJx0eshfY4"
r = requests.get(
    'http://localhost:3000/datasets',
     headers={'Authorization': 'Bearer {}'.format(API_KEY)}
)
print(r.url)
response = r.json()
print(response)
```


