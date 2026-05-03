from sharks.app import app


def main() -> None:
    import os

    import uvicorn

    reload_enabled = os.getenv("APP_RELOAD", "false").lower() in {"1", "true", "yes", "on"}
    uvicorn.run("sharks.app:app", host="0.0.0.0", port=8000, reload=reload_enabled)


if __name__ == "__main__":
    main()
