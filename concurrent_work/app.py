import logging

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from concurrent_work.server import Server

app = FastAPI(debug=True)
server = Server()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
# alab
@app.post('/alab/start')
async def start_alab():
    return server.start_alab()


@app.post('/alab/stop')
async def stop_alab():
    return server.stop_alab()


@app.post('/diag/start')
async def start_diag():
    return server.start_diag()


@app.post('/diag/stop')
async def stop_diag():
    return server.stop_diag()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
