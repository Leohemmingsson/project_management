# own
from . import v1
from . import no_version_routes

from .shared_models import get_session
from .orm import User
from .scheduled import server_maintanance

# pip
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from apscheduler.schedulers.background import BackgroundScheduler


app = FastAPI(
    title="Project management",
    version="0.1.0",
    redoc_url=None,
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def bootstrap_admin_user():
    with get_session() as session:
        all_users = User.get_all(session)
        if len(all_users) < 1:
            env = dotenv_values(".env")

            if env["ADMIN_PASSWORD"]:
                ADMIN_PASSWORD = env["ADMIN_PASSWORD"]
            else:
                raise Exception("ADMIN_PASSWORD not set")
            ADMIN_EMAIL = env["ADMIN_EMAIL"]

            user = {
                "name": "admin",
                "password": ADMIN_PASSWORD,
                "email": ADMIN_EMAIL,
                "authorization": "S",
            }
            admin_user = User.add(session=session, **user)
            print("Created admin user")
            print(admin_user)


@app.on_event("startup")
def on_startup():
    bootstrap_admin_user()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(server_maintanance, "interval", hours=1)
    scheduler.start()


for page in no_version_routes.__all__:
    router = getattr(no_version_routes, page)
    app.include_router(router, prefix="")

for page in v1.__all__:
    router = getattr(v1, page)
    app.include_router(router, prefix="/V1")
