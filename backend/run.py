from app.main import app

import uvicorn


if __name__ == "__main__":
    import os

    mode = os.getenv("MODE", "prod")

    if mode == "prod":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif mode == "dev":
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print(f"Mode {mode} does not exist")
