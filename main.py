""" (script)
This is the main file for the api
This is the file that runs the code
It imports the routers and adds them to the api
"""

__authors__ = ["Siddhesh Zantye", "Dhruv Rayat"]
__version__ = "0.0.1"

import uvicorn

from models import OSC_API
from api import home, oauth, users


app = OSC_API()


# Main function (to run the api)
def main():
    # Routers
    app.include_router(home)
    app.include_router(oauth)
    app.include_router(users)

    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


# Run
if __name__ == "__main__":
    main()
