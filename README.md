# RFCRM - basic api based crm/cms

## Build the app image

To build, run and test the application you'll need `docker-compose`. First, build the image.

```
$ docker-compose build
```

## Run the app container

Now, let's run the previously built image. This command will run a docker container in the background.

```
$ docker-compose run -d
```

Alternatively, you can build and run in one go like so.

```
$ docker-compose run --build -d
```

## Run the tests

Running tests is as easy as

```
$ docker-compose exec web poetry run pytest
```
