import logging

import uvicorn

import config
from api import Api
from gram import Gram
from identity_manager import IdentityManager

app = Api(Gram(IdentityManager(config.IDENTITY_DB)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    config = uvicorn.Config("main:app", host='0.0.0.0', port=5000, log_level="debug", lifespan='on')
    server = uvicorn.Server(config)
    server.run()
