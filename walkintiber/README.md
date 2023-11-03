# Walkin' Tiber

## the API gateway

to test the django microservice only endpoints run the following command:

    python walkintiber/manage.py runserver 0.0.0.0:8001

then test the endpoints using [this](https://www.postman.com/andreagalle/workspace/my-workspace/collection/30905772-552a27e5-df0e-4b8c-8bc5-7ff9bd69e300?action=share&creator=30905772) Postman collection or (for simpler requests) copy/paste URLs like this:

    http://localhost:8001/osmclient/get_buildings/?bbox=41.8828000,12.4642000,41.8964000,12.481900

or 

    http://localhost:8001/osmclient/get_highways/?bbox=41.8828000,12.4642000,41.8964000,12.481900

## the Docker stack

to run this project, execute the following commands:

### start

    docker-compose up --build

otherwise (for newer verisions of Docker, i.e. withespace in place of `-` dash)

    docker compose up --build


### stop

    docker-compose down

otherwise (for newer verisions of Docker, i.e. withespace in place of `-` dash)

    docker compose down

Once the whole stack is up & running you can issue requests to the server through the django webapp admin console. 