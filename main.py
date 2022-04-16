""" (script)
This is the main file for the api
This is the file that runs the code
It imports the routers and adds them to the api
"""

__authors__ = ["Siddhesh Zantye", "Dhruv Rayat"]
__version__ = "0.0.1"

import asyncio
import uvicorn

from models import OSC_API
from api import home, oauth, users
from api.auth.create_user import create_super_user, create_user, create_database


app = OSC_API()

# Routers
app.include_router(home)
app.include_router(oauth)
app.include_router(users)

# Run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)