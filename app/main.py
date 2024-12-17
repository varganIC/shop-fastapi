import uvicorn
from fastapi import Depends, FastAPI

from api_routes import (
    auth,
    bucket,
    categories,
    metadata,
    product,
    view_prouct_categories
)
from service_auth.auth import verify_token
from settings.settings_loader import uvicorn_settings

app = FastAPI(title=metadata.title)

PROTECTED = [Depends(verify_token)]


app.include_router(auth.router, dependencies=[])
app.include_router(product.router, dependencies=PROTECTED)
app.include_router(bucket.router, dependencies=[])
app.include_router(categories.router, dependencies=PROTECTED)
app.include_router(view_prouct_categories.router, dependencies=[])


if __name__ == "__main__":
    uvicorn.run(app, **uvicorn_settings)
