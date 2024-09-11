from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn import run as uvicorn_run

from api import router_v1
from core import app_settings, logger_config
from middlewares import bearer_authorization
from utils.constants import TAG_AUTH, TAG_FILES, TAG_HEALTHCHECK


app = FastAPI(
    title=app_settings.app_title,
    lifespan=app_settings.app_lifespan,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {'name': TAG_HEALTHCHECK},
        {'name': TAG_AUTH},
        {'name': TAG_FILES}
    ]
)

app.middleware('http')(bearer_authorization)

app.include_router(router_v1, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn_run('main:app',
                host='0.0.0.0',
                port=8000,
                log_config=logger_config,
                reload=True,
                reload_dirs=['src'])
