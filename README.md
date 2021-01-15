# LXP Recommendation Service

## Local development setup

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
coverage run manage.py test --settings=lxp_recommendation_service.settings.test
coverage report -m
coverage html -d cover
```
