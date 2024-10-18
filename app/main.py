import uvicorn
from fastapi import FastAPI

from api_routes import metadata
from settings.settings_loader import uvicorn_settings


app = FastAPI(title=metadata.title)


if __name__ == "__main__":
    uvicorn.run(app, **uvicorn_settings)
