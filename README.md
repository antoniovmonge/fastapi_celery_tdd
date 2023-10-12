# FastAPI + Celery with Test Driven Development practice

## Description

This is a practice project to learn how to use FastAPI and Celery with Test Driven Development.

## Run the app without Docker

```bash
uvicorn main:app --reload
```

## Run the app with Docker

```bash
docker-compose build
```

```bash
docker-compose up
```

See the logs

```bash
docker-compose logs -f
```

## Useful commands

Entering the Python shell of the running `web` service.

```bash
docker-compose exec web python
```

```bash
>>> from main import app
>>> from project.users.tasks import divide
>>>
>>> divide.delay(1, 2)
```

Logs of the Celery worker:

```bash
docker-compose logs celery_worker
```

Enter the shell of the `redis` service:

```bash
docker-compose exec redis sh
```

```bash
redis-cli
```

Replace the ID with the ID of the task to check

```bash
127.0.0.1:6379> MGET celery-task-meta-<ID>
```
