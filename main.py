import uvicorn
from fastapi import FastAPI

from api import router as api_router
from redis import cache


app = FastAPI()

app.include_router(api_router, prefix='/api')


@app.on_event('startup')
async def startup_event():
    await cache.init()


@app.on_event('shutdown')
async def startup_event():
    await cache.close()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
