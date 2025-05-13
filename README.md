# Project management
## Setup
1. Create `.env` files:
```
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=pass
DB_NAME=management_db
```
> In root of project

```
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=pass
DB_NAME=management_db
```
> In backend/

2. To setup the project in dev either start the whole project:
```bash
docker compose up --build
```
Or choose:
```bash
docker compose up --build service1 service2 # Obs this does not work if anything depends on external service

docker compose up --build --no-deps service1 service2 # If there is depends_on
```

3. Setup DB

```fish
set -x DB_URL "mysql+pymysql://user:password@localhost:3306/your_db" # This can be skipped if using docker compose db

alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```
