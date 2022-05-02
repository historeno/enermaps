# Launch the service

Run this command : 

```
docker-compose --file docker-compose-db.yml up --build
```

The database is available on host 127.0.0.1 
and port 5433 with the psql
client (see ![](db/README.md))


# pgAdmin acess

```markdown
host : 127.0.0.1
Port : 5433
Maintenance database : postgres
Username : test (or see .env-db)
DB_PASSWORD : example (or see .env-db)
```