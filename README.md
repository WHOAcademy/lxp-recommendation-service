# LXP Recommendation Service

## Local development setup

To spin up a postgressql via docker:

`
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=balthazar -e POSTGRES_USER=bastian -e POSTGRES_DB=neverendingblog -d postgres
`

To spin up a redis via docker:

`
docker run --name redis -p 6379:6379 -d redis
`

For Linux/macOS:
```
export APP_ENV="local"
export SECRET_KEY="abcd"
```

For Windows:
```
SET APP_ENV=local
SET SECRET_KEY=abcd
```

### Running the tests 

```
export TEST_DATABASE_SERVICE_HOST="localhost"
export TEST_DATABASE_SERVICE_PORT="5432"

python manage.py test --settings=lxp_recommendation_service.settings.test
```
