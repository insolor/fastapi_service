import uvicorn
from decouple import config

from inside.app import app

PORT = config("PORT", default=10000)
uvicorn.run(app, host="0.0.0.0", port=PORT)
